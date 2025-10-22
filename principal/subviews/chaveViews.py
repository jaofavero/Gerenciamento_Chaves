from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from principal.models import HistoricoEmprestimo, Chave, Usuario # Importamos modelos necessários
from django.views.decorators.http import require_POST


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
    GET: Exibe a página de confirmação.
    POST: Registra a posse da chave para o usuário logado.
    """
    chave = get_object_or_404(Chave, pk=pk)
    usuario_logado = request.user

    if request.method == 'POST':
        if chave.portador_atual != usuario_logado:
            HistoricoEmprestimo.objects.create(
                chave=chave,
                usuario=usuario_logado,
                acao='adquirida' 
            )
        return redirect('index')
    
    else: 
        contexto = {
            'chave': chave
        }
        return render(request, 'ativos/chaves/chave.html', contexto)

@login_required
@require_POST # Garante que esta view só aceite requisições POST
def receber_chave(request, pk):
    """
    View para a ação de Staff "Receber Chave" (Devolução).
    Muda o status da chave para 'disponivel' e registra no histórico.
    *** RESTRITA APENAS PARA STAFF E MÉTODO POST ***
    """
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
    """
    View para a página de "Entregar Chave".
    GET: Exibe a página com busca de usuários.
    POST: Atribui a chave ao usuário selecionado.
    *** RESTRITA APENAS PARA STAFF ***
    """
    # 1. Verificação de Staff
    if not request.user.is_staff:
        return redirect('index')

    # 2. Busca a chave
    chave = get_object_or_404(Chave, pk=pk)
    contexto = {'chave': chave}
    
    # 3. Lógica do POST (Quando o staff seleciona um usuário)
    if request.method == 'POST':
        usuario_id = request.POST.get('usuario_id')
        if not usuario_id:
            # Lidar com erro se nenhum usuário foi enviado
            contexto['erro'] = "Nenhum usuário selecionado."
            return render(request, 'ativos/chaves/entregar_chave.html', contexto)

        try:
            usuario_selecionado = Usuario.objects.get(pk=usuario_id)
        except Usuario.DoesNotExist:
            contexto['erro'] = "Usuário selecionado não encontrado."
            return render(request, 'ativos/chaves/entregar_chave.html', contexto)

        # 4. Cria o registro de "adquirida" para o usuário selecionado
        # O modelo 'HistoricoEmprestimo'
        # cuida de mudar o status da chave e o portador_atual.
        HistoricoEmprestimo.objects.create(
            chave=chave,
            usuario=usuario_selecionado, # O usuário que RECEBEU
            acao='adquirida'
        )
        
        # 5. Redireciona de volta para a lista de chaves
        return redirect(request.GET.get('next', 'lista_chaves'))

    # 6. Lógica do GET (Exibir a página de busca)
    else:
        busca_termo = request.GET.get('busca_usuario', '')
        usuarios_encontrados = None

        if busca_termo:
            # Busca por username, nome ou sobrenome
            usuarios_encontrados = Usuario.objects.filter(
                Q(username__icontains=busca_termo) |
                Q(first_name__icontains=busca_termo) |
                Q(last_name__icontains=busca_termo)
            ).filter(is_active=True) # Busca apenas usuários ativos
        
        contexto['usuarios_encontrados'] = usuarios_encontrados
        contexto['busca_termo'] = busca_termo
        return render(request, 'ativos/chaves/entregar_chave.html', contexto)