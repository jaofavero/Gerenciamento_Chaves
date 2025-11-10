# Author: João Victor Marques Favero

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from principal.models import HistoricoEmprestimo, Chave, Usuario  # Importa os modelos necessários

@login_required
def historico_list(request):
    """
    View para a Tela de Histórico.
    *** RESTRITA APENAS PARA STAFF ***
    """
    # Redireciona usuários não staff para a página inicial
    if not request.user.is_staff:
        return redirect('index')
    
    # Obtém todos os registros de empréstimo, ordenados por data/hora
    queryset = HistoricoEmprestimo.objects.select_related('chave', 'usuario').order_by('-data_hora')

    # --- Lógica de Filtro/Pesquisa  ---
    chave_nome = request.GET.get('chave_nome')  # Nome da chave para filtro
    usuario_nome = request.GET.get('usuario_nome')  # Nome do usuário para filtro
    acao = request.GET.get('acao')  # Ação para filtro
    data = request.GET.get('data')  # Data para filtro
    if chave_nome: queryset = queryset.filter(chave__nome__icontains=chave_nome)  # Filtro por nome da chave
    if usuario_nome: queryset = queryset.filter(Q(usuario__username__icontains=usuario_nome) | 
                                                Q(usuario__first_name__icontains=usuario_nome) | 
                                                Q(usuario__last_name__icontains=usuario_nome))  # Filtro por nome do usuário
    if acao: queryset = queryset.filter(acao=acao)  # Filtro por ação
    if data: queryset = queryset.filter(data_hora__date=data)  # Filtro por data

    # --- Lógica de Paginação  ---
    paginador = Paginator(queryset, 20)  # Pagina os resultados em grupos de 20
    pagina_num = request.GET.get('page')  # Obtém o número da página atual
    page_obj = paginador.get_page(pagina_num)  # Obtém os objetos da página atual

    get_params = request.GET.copy()
    if 'page' in get_params:
        del get_params['page']
    get_params_url = get_params.urlencode()
    
    contexto = {
        'page_obj': page_obj,  # Objeto da página atual
        'emprestimos_list': page_obj.object_list,  # Lista de empréstimos da página atual
        'get_params_url': get_params_url
    }
    return render(request, 'historico/historico.html', contexto)  # Renderiza a template com o contexto

@login_required
def api_ultimos_emprestimos(request):
    """
    View 'API' especial (para atualização da index de staff).
    """
    # Obtém os últimos 20 empréstimos
    emprestimos = HistoricoEmprestimo.objects.select_related('chave', 'usuario').order_by('-data_hora')[:20]
    contexto = {
        'emprestimos_list': emprestimos  # Lista de empréstimos para a API
    }
    return render(request, 'historico/_lista_emprestimos.html', contexto)  # Renderiza a template da lista de empréstimos