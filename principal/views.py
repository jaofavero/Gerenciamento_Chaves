from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
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

''''@login_required'''
def pegar_chave(request, pk):
    """
    View para a página individual da Chave.
    GET: Exibe a página de confirmação.
    POST: Registra a posse da chave para o usuário logado.
    """
    # Busca a chave específica pelo ID (pk) ou retorna um erro 404 se não existir
    chave = get_object_or_404(Chave, pk=pk)
    usuario_logado = request.user

    if request.method == 'POST':
        # --- Lógica do Botão "Estou com a posse da chave" ---
        
        # Apenas cria o registro se o usuário logado não for o portador atual
        if chave.portador_atual != usuario_logado:
            
            # Cria o novo registro de histórico.
            # A ação 'adquirida' acionará o método .save() 
            # do modelo HistoricoEmprestimo, que atualizará
            # o status e o portador da chave automaticamente.
            HistoricoEmprestimo.objects.create(
                chave=chave,
                usuario=usuario_logado,
                acao='adquirida' 
            )
        
        # Redireciona o usuário de volta para a tela inicial
        return redirect('index')
    
    else: # request.method == 'GET'
        # --- Lógica para exibir a página ---
        # Apenas exibe a página de confirmação
        contexto = {
            'chave': chave
        }
        # Renderiza o template que criamos no Passo 1
        return render(request, 'ativos/chaves/chave.html', contexto)