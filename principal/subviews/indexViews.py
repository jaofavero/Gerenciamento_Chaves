# Author: João Victor Marques Favero
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from principal.models import HistoricoEmprestimo, Chave  # Importa os modelos necessários

@login_required
def index(request):
    """
    View para a Tela Inicial.
    Exibe uma lista paginada de todas as chaves
    e, para staff, os 10 últimos registros do histórico.
    """
    # 1. Lógica da Tabela de Chaves
    queryset = Chave.objects.select_related('portador_atual').filter(excluido=False).order_by('nome')  # Obtém chaves não excluídas
    chave_nome = request.GET.get('chave_nome')  # Obtém o nome da chave da query string
    if chave_nome:
        queryset = queryset.filter(nome__icontains=chave_nome)  # Filtra chaves pelo nome se fornecido
    
    paginador = Paginator(queryset, 20)  # Pagina as chaves em grupos de 20
    pagina_num = request.GET.get('page')  # Obtém o número da página da query string
    page_obj = paginador.get_page(pagina_num)  # Obtém o objeto da página atual

    # Copia os parâmetros GET para não modificar o original
    get_params = request.GET.copy()
    if 'page' in get_params:
        del get_params['page']  # Remove o parâmetro 'page' existente
    
    # URL de parâmetros filtrada (ex: "chave_nome=teste")
    get_params_url = get_params.urlencode()
    # 2. Contexto inicial
    contexto = {
        'page_obj': page_obj,  # Adiciona o objeto da página ao contexto
        'chaves_list': page_obj.object_list  # Adiciona a lista de chaves ao contexto
    }

    # 3. Busca os últimos 10 empréstimos SE o usuário for staff
    if request.user.is_staff:
        ultimos_emprestimos = HistoricoEmprestimo.objects.select_related(
            'chave', 'usuario'
        ).order_by('-data_hora')[:10]  # Obtém os últimos 10 empréstimos
        
        # Adiciona a lista ao contexto
        contexto['ultimos_10_emprestimos'] = ultimos_emprestimos

    return render(request, 'index.html', contexto)  # Renderiza a página com o contexto