from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from principal.models import HistoricoEmprestimo, Chave # Importamos modelos necessários

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
    return render(request, 'ativos/chaves/lista_chaves.html', contexto)

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