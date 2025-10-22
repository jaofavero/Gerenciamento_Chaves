from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from principal.models import HistoricoEmprestimo, Chave, Usuario # Importamos modelos necessários

@login_required
def historico_list(request):
    """
    View para a Tela de Histórico.
    *** RESTRITA APENAS PARA STAFF ***
    """
    if not request.user.is_staff:
        return redirect('index')
    
    queryset = HistoricoEmprestimo.objects.select_related('chave', 'usuario').order_by('-data_hora')

    # --- Lógica de Filtro/Pesquisa  ---
    chave_nome = request.GET.get('chave_nome')
    usuario_nome = request.GET.get('usuario_nome')
    acao = request.GET.get('acao')
    data = request.GET.get('data')
    if chave_nome: queryset = queryset.filter(chave__nome__icontains=chave_nome)
    if usuario_nome: queryset = queryset.filter(Q(usuario__username__icontains=usuario_nome) | Q(usuario__first_name__icontains=usuario_nome) | Q(usuario__last_name__icontains=usuario_nome))
    if acao: queryset = queryset.filter(acao=acao)
    if data: queryset = queryset.filter(data_hora__date=data)

    # --- Lógica de Paginação  ---
    paginador = Paginator(queryset, 20) 
    pagina_num = request.GET.get('page')
    page_obj = paginador.get_page(pagina_num)

    contexto = {
        'page_obj': page_obj,
        'emprestimos_list': page_obj.object_list 
    }
    return render(request, 'historico/historico.html', contexto)

@login_required
def api_ultimos_emprestimos(request):
    """
    View 'API' especial (para atualização da index de staff).
    """
    emprestimos = HistoricoEmprestimo.objects.select_related('chave', 'usuario').order_by('-data_hora')[:20]
    contexto = {
        'emprestimos_list': emprestimos
    }
    return render(request, 'historico/_lista_emprestimos.html', contexto)