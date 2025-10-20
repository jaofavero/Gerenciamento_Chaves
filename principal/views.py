from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q
from principal.models import HistoricoEmprestimo, Chave, Usuario

def index(request):
    """
    View para a Tela Inicial.
    """
    emprestimos = HistoricoEmprestimo.objects.select_related('chave', 'usuario').order_by('-data_hora')[:20]
    contexto = {
        # MUDANÇA: Usar 'emprestimos_list' como chave
        'emprestimos_list': emprestimos 
    }
    return render(request, 'index.html', contexto) # Caminho já corrigido

def historico_list(request):
    """
    View para a Tela de Histórico.
    """
    queryset = HistoricoEmprestimo.objects.select_related('chave', 'usuario').order_by('-data_hora')

    # --- Lógica de Filtro/Pesquisa (sem alterações) ---
    chave_nome = request.GET.get('chave_nome')
    usuario_nome = request.GET.get('usuario_nome')
    acao = request.GET.get('acao')
    data = request.GET.get('data')
    if chave_nome: queryset = queryset.filter(chave__nome__icontains=chave_nome)
    if usuario_nome: queryset = queryset.filter(Q(usuario__username__icontains=usuario_nome) | Q(usuario__first_name__icontains=usuario_nome) | Q(usuario__last_name__icontains=usuario_nome))
    if acao: queryset = queryset.filter(acao=acao)
    if data: queryset = queryset.filter(data_hora__date=data)

    # --- Lógica de Paginação (sem alterações) ---
    paginador = Paginator(queryset, 20) 
    pagina_num = request.GET.get('page')
    page_obj = paginador.get_page(pagina_num)

    contexto = {
        'page_obj': page_obj,
        # MUDANÇA: Adicionar a lista de empréstimos da página atual com a chave padronizada
        'emprestimos_list': page_obj.object_list 
    }
    return render(request, 'historico/historico.html', contexto) # Caminho já correto

def api_ultimos_emprestimos(request):
    """
    View 'API' especial.
    """
    emprestimos = HistoricoEmprestimo.objects.select_related('chave', 'usuario').order_by('-data_hora')[:20]
    contexto = {
        # MUDANÇA: Usar 'emprestimos_list' como chave (já estava assim antes, mas confirmando)
        'emprestimos_list': emprestimos
    }
    return render(request, 'historico/_lista_emprestimos.html', contexto) # Caminho já corrigido