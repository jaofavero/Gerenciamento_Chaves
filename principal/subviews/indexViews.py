from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from principal.models import HistoricoEmprestimo, Chave # Importamos direto dos models consolidados

@login_required
def index(request):
    """
    View para a Tela Inicial.
    Exibe uma lista paginada de todas as chaves
    e, para staff, os 10 últimos registros do histórico.
    """
    # 1. Lógica da Tabela de Chaves
    queryset = Chave.objects.select_related('portador_atual').filter(excluido=False).order_by('nome')
    chave_nome = request.GET.get('chave_nome')
    if chave_nome:
        queryset = queryset.filter(nome__icontains=chave_nome)
    
    paginador = Paginator(queryset, 20) 
    pagina_num = request.GET.get('page')
    page_obj = paginador.get_page(pagina_num)

    # 2. Contexto inicial
    contexto = {
        'page_obj': page_obj,
        'chaves_list': page_obj.object_list 
    }

    # 3. Busca os últimos 10 empréstimos SE o usuário for staff
    if request.user.is_staff:
        ultimos_emprestimos = HistoricoEmprestimo.objects.select_related(
            'chave', 'usuario'
        ).order_by('-data_hora')[:10]
        
        # Adiciona a lista ao contexto
        contexto['ultimos_10_emprestimos'] = ultimos_emprestimos

    return render(request, 'index.html', contexto)