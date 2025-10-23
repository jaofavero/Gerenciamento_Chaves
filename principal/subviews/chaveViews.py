from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from principal.models import HistoricoEmprestimo, Chave, Usuario # Importamos modelos necessários
from django.views.decorators.http import require_POST
from django.contrib import messages


@login_required
def lista_chaves(request):
    """
    View para a Tela de Gerenciamento de Chaves.
    Lista todas as chaves com filtros.
    *** RESTRITA APENAS PARA STAFF ***
    """
    # 1. Verificação de staff
    if not request.user.is_staff:
        return redirect('index')

    # 2. Busca base (mostra todas as chaves, ordenadas por nome)
    queryset = Chave.objects.select_related('portador_atual').order_by('nome')

    # 3. Lógica de Filtro/Pesquisa
    chave_nome = request.GET.get('chave_nome')
    status = request.GET.get('status')
    excluido = request.GET.get('excluido')

    if chave_nome: 
        queryset = queryset.filter(nome__icontains=chave_nome)
    if status: 
        queryset = queryset.filter(status=status)
    if excluido == 'sim':
        queryset = queryset.filter(excluido=True)
    elif excluido == 'nao':
        queryset = queryset.filter(excluido=False)

    # 4. Lógica de Paginação
    paginador = Paginator(queryset, 20) 
    pagina_num = request.GET.get('page')
    page_obj = paginador.get_page(pagina_num)

    contexto = {
        'page_obj': page_obj,
        'chaves_list': page_obj.object_list 
    }
    return render(request, 'ativos/chaves/_lista_chaves.html', contexto)

@login_required
def pegar_chave(request, pk):
    """
    View para a página individual da Chave.
    GET: Exibe a página de confirmação (com AVISO de permissão).
    POST: Registra a posse da chave (sem verificação de permissão).
    """
    chave = get_object_or_404(Chave.objects.select_related('portador_atual').prefetch_related('grupos_permissao'), pk=pk)
    usuario_logado = request.user

    if request.method == 'POST':
        # --- LÓGICA DO POST ---
        # A VERIFICAÇÃO DE PERMISSÃO FOI REMOVIDA CONFORME SOLICITADO.
        # A única permissão é @login_required.

        if chave.portador_atual != usuario_logado:
            HistoricoEmprestimo.objects.create(
                chave=chave,
                usuario=usuario_logado,
                acao='adquirida' 
            )
        return redirect('index')
    
    else: 
        grupos_requeridos_ids = set(chave.grupos_permissao.values_list('pk', flat=True))
        
        tem_permissao_grupo = False
        if not grupos_requeridos_ids:
            tem_permissao_grupo = True # Chave não tem restrição
        else:
            grupos_usuario_ids = set(usuario_logado.groups.values_list('pk', flat=True))
            tem_permissao_grupo = not grupos_requeridos_ids.isdisjoint(grupos_usuario_ids)
        
        # Se a chave EXIGE grupos e o usuário NÃO está em NENHUM deles
        if grupos_requeridos_ids and not tem_permissao_grupo:
            nomes_grupos = ", ".join(g.name for g in chave.grupos_permissao.all())
            messages.warning(request, f"Aviso: Você não faz parte de nenhum grupo com permissão para acessar essa chave. Grupos: '{nomes_grupos}'.")

        contexto = {
            'chave': chave
        }
        return render(request, 'ativos/chaves/chave.html', contexto)

@login_required
@require_POST # Garante que esta view só aceite requisições POST
def receber_chave(request, pk):

    # 1. Verificação de Staff
    if not request.user.is_staff:
        return redirect('index')

    # 2. Busca a chave
    chave = get_object_or_404(Chave, pk=pk)
    
    # 3. Pega o usuário que estava com a chave (para o registro)
    usuario_que_devolveu = chave.portador_atual
    
    # 4. Cria o registro de devolução
    # O modelo 'HistoricoEmprestimo' 
    # no seu método save() cuida de mudar o status da chave.
    HistoricoEmprestimo.objects.create(
        chave=chave,
        usuario=usuario_que_devolveu, # Registra quem devolveu
        acao='devolucao'
    )
    
    # 5. Redireciona de volta para a lista de chaves
    # Tenta redirecionar para a página de onde o staff veio
    next_url = request.GET.get('next', 'lista_chaves')
    if next_url != 'index':
         next_url = 'lista_chaves' # Garante que só volte para index ou lista_chaves
         
    return redirect(next_url)


@login_required
def entregar_chave(request, pk):

    # 1. Verificação de Staff
    if not request.user.is_staff:
        return redirect('index')

    # 2. Busca a chave
    chave = get_object_or_404(Chave, pk=pk)
    contexto = {'chave': chave}
    
    # 3. Lógica do POST (Quando o staff seleciona um usuário)
    if request.method == 'POST':
        # ... (A LÓGICA DO POST CONTINUA IGUAL) ...
        usuario_id = request.POST.get('usuario_id')
        if not usuario_id:
            contexto['erro'] = "Nenhum usuário selecionado."
            # (Precisamos recarregar a lista de usuários aqui também em caso de erro)
            queryset = Usuario.objects.filter(is_active=True).prefetch_related('groups').order_by('username')
            paginador = Paginator(queryset, 20)
            page_obj = paginador.get_page(request.GET.get('page'))
            contexto['page_obj'] = page_obj
            return render(request, 'ativos/chaves/entregar_chave.html', contexto)

        try:
            usuario_selecionado = Usuario.objects.get(pk=usuario_id)
        except Usuario.DoesNotExist:
            contexto['erro'] = "Usuário selecionado não encontrado."
            # (Recarregar a lista de usuários)
            queryset = Usuario.objects.filter(is_active=True).prefetch_related('groups').order_by('username')
            paginador = Paginator(queryset, 20)
            page_obj = paginador.get_page(request.GET.get('page'))
            contexto['page_obj'] = page_obj
            return render(request, 'ativos/chaves/entregar_chave.html', contexto)

        HistoricoEmprestimo.objects.create(
            chave=chave,
            usuario=usuario_selecionado,
            acao='adquirida'
        )
        
        return redirect(request.GET.get('next', 'lista_chaves'))

    # 4. LÓGICA DO GET (Exibir a página de busca E lista)
    else:
        # Pega o termo de busca (pode estar vazio)
        busca_termo = request.GET.get('busca_usuario', '')
        
        # Começa com todos os usuários ativos
        queryset = Usuario.objects.filter(is_active=True).prefetch_related('groups').order_by('username')

        # Se houver um termo de busca, filtra o queryset
        if busca_termo:
            queryset = queryset.filter(
                Q(username__icontains=busca_termo) |
                Q(first_name__icontains=busca_termo) |
                Q(last_name__icontains=busca_termo)
            )
        
        # Pagina o resultado (filtrado ou não)
        paginador = Paginator(queryset, 20) # 20 usuários por página
        pagina_num = request.GET.get('page')
        page_obj = paginador.get_page(pagina_num)
        
        # Pega o grupo de permissão da chave
        grupos_requeridos_ids = set(chave.grupos_permissao.values_list('pk', flat=True))
        
        # Gera a lista de nomes para o template
        nomes_grupos = ", ".join(g.name for g in chave.grupos_permissao.all())

        # Se a chave não tem grupos definidos, todos têm permissão
        if not grupos_requeridos_ids:
            for usuario in page_obj.object_list:
                usuario.tem_permissao = True
        else:
            # Se a chave tem grupos, verifica a intersecção
            for usuario in page_obj.object_list:
                grupos_usuario_ids = set(usuario.groups.values_list('pk', flat=True))
                # .isdisjoint() é rápido e verifica se não há nenhum item em comum
                usuario.tem_permissao = not grupos_requeridos_ids.isdisjoint(grupos_usuario_ids)
        
        contexto['page_obj'] = page_obj
        contexto['busca_termo'] = busca_termo
        contexto['nomes_grupos_requeridos'] = nomes_grupos # 3. PASSA OS NOMES PARA O TEMPLATE
        return render(request, 'ativos/chaves/entregar_chave.html', contexto)