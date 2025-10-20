from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q
from principal.models import HistoricoEmprestimo, Chave, Usuario

def index(request):
    """
    View para a Tela Inicial.
    Busca os 20 últimos registros de histórico.
    """
    # Usamos select_related para otimizar a busca, pegando dados de Chave e Usuario
    # na mesma consulta ao banco de dados.
    emprestimos = HistoricoEmprestimo.objects.select_related('chave', 'usuario').order_by('-data_hora')[:20]
    
    contexto = {
        'emprestimos': emprestimos
    }
    return render(request, '/index.html', contexto)

def historico_list(request):
    """
    View para a Tela de Histórico.
    Busca todos os registros, aplicando filtros de pesquisa e paginação.
    """
    
    # Começamos com todos os registros, otimizados com select_related
    queryset = HistoricoEmprestimo.objects.select_related('chave', 'usuario').order_by('-data_hora')

    # --- Lógica de Filtro/Pesquisa ---
    chave_nome = request.GET.get('chave_nome')
    usuario_nome = request.GET.get('usuario_nome')
    acao = request.GET.get('acao')
    data = request.GET.get('data')

    if chave_nome:
        # __icontains faz uma busca "case-insensitive" (não diferencia maiúsculas/minúsculas)
        queryset = queryset.filter(chave__nome__icontains=chave_nome)
    
    if usuario_nome:
        # Usamos Q para pesquisar em múltiplos campos (username, first_name, last_name)
        queryset = queryset.filter(
            Q(usuario__username__icontains=usuario_nome) |
            Q(usuario__first_name__icontains=usuario_nome) |
            Q(usuario__last_name__icontains=usuario_nome)
        )

    if acao:
        queryset = queryset.filter(acao=acao)
        
    if data:
        # __date filtra apenas pela parte da data, ignorando a hora
        queryset = queryset.filter(data_hora__date=data)

    # --- Lógica de Paginação ---
    # Mostra 20 itens por página, conforme solicitado
    paginador = Paginator(queryset, 20) 
    pagina_num = request.GET.get('page')
    page_obj = paginador.get_page(pagina_num)

    contexto = {
        'page_obj': page_obj
        # Os parâmetros de request (request.GET) são passados automaticamente
        # para o template, por isso a pesquisa e paginação funcionam juntas.
    }
    return render(request, 'historico/historico.html', contexto)

def api_ultimos_emprestimos(request):
    """
    View 'API' especial.
    Retorna APENAS o HTML da tabela dos 20 últimos empréstimos.
    Usado pelo JavaScript da Tela Inicial para atualização automática.
    """
    emprestimos = HistoricoEmprestimo.objects.select_related('chave', 'usuario').order_by('-data_hora')[:20]
    contexto = {
        'emprestimos': emprestimos
    }
    # Renderiza apenas o template parcial
    return render(request, '/historico/_lista_emprestimos.html', contexto)