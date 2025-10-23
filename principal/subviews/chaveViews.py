# Author: João Victor Marques Favero

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from principal.models import HistoricoEmprestimo, Chave, Usuario
from django.views.decorators.http import require_POST
from django.contrib import messages

# Lista e filtra chaves para staff, com paginação
@login_required
def lista_chaves(request):
    """
    Tela de Gerenciamento de Chaves (apenas staff).
    Lista com filtros e paginação.
    """
    if not request.user.is_staff:
        return redirect('index')

    queryset = Chave.objects.select_related('portador_atual').order_by('nome')

    # Filtros por nome, status e exclusão
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

    # Paginação
    paginador = Paginator(queryset, 20)
    pagina_num = request.GET.get('page')
    page_obj = paginador.get_page(pagina_num)

    contexto = {
        'page_obj': page_obj,
        'chaves_list': page_obj.object_list
    }
    return render(request, 'ativos/chaves/_lista_chaves.html', contexto)

# Página da chave: GET mostra aviso; POST registra aquisição pelo usuário logado
@login_required
def pegar_chave(request, pk):
    """
    Página individual da Chave.
    GET: mostra confirmação e possíveis avisos de permissão.
    POST: registra aquisição da chave (apenas login exigido).
    """
    chave = get_object_or_404(
        Chave.objects.select_related('portador_atual').prefetch_related('grupos_permissao'),
        pk=pk
    )
    usuario_logado = request.user

    if request.method == 'POST':
        # Sem checagem de grupo no POST: apenas login
        if chave.portador_atual != usuario_logado:
            HistoricoEmprestimo.objects.create(
                chave=chave,
                usuario=usuario_logado,
                acao='adquirida'
            )
        return redirect('index')

    else:
        # Verifica interseção entre grupos da chave e do usuário
        grupos_requeridos_ids = set(chave.grupos_permissao.values_list('pk', flat=True))

        if not grupos_requeridos_ids:
            tem_permissao_grupo = True  # Sem restrição
        else:
            grupos_usuario_ids = set(usuario_logado.groups.values_list('pk', flat=True))
            tem_permissao_grupo = not grupos_requeridos_ids.isdisjoint(grupos_usuario_ids)

        # Mostra aviso se a chave exigir grupos e o usuário não tiver nenhum
        if grupos_requeridos_ids and not tem_permissao_grupo:
            nomes_grupos = ", ".join(g.name for g in chave.grupos_permissao.all())
            messages.warning(
                request,
                f"Aviso: Você não faz parte de nenhum grupo com permissão para acessar essa chave. Grupos: '{nomes_grupos}'."
            )

        contexto = {'chave': chave}
        return render(request, 'ativos/chaves/chave.html', contexto)

# Receber (devolução) de chave por staff; apenas POST
@login_required
@require_POST
def receber_chave(request, pk):
    if not request.user.is_staff:
        return redirect('index')

    chave = get_object_or_404(Chave, pk=pk)
    usuario_que_devolveu = chave.portador_atual

    # Registro de devolução (o save() no modelo ajusta status/portador)
    HistoricoEmprestimo.objects.create(
        chave=chave,
        usuario=usuario_que_devolveu,
        acao='devolucao'
    )

    # Redireciona apenas para index ou lista_chaves
    next_url = request.GET.get('next', 'lista_chaves')
    if next_url != 'index':
        next_url = 'lista_chaves'
    return redirect(next_url)

# Entregar chave a um usuário (seleção e atribuição) por staff
@login_required
def entregar_chave(request, pk):
    if not request.user.is_staff:
        return redirect('index')

    chave = get_object_or_404(Chave, pk=pk)
    contexto = {'chave': chave}

    # POST: staff seleciona o usuário que receberá a chave
    if request.method == 'POST':
        usuario_id = request.POST.get('usuario_id')
        if not usuario_id:
            contexto['erro'] = "Nenhum usuário selecionado."
            queryset = Usuario.objects.filter(is_active=True).prefetch_related('groups').order_by('username')
            paginador = Paginator(queryset, 20)
            page_obj = paginador.get_page(request.GET.get('page'))
            contexto['page_obj'] = page_obj
            return render(request, 'ativos/chaves/entregar_chave.html', contexto)

        try:
            usuario_selecionado = Usuario.objects.get(pk=usuario_id)
        except Usuario.DoesNotExist:
            contexto['erro'] = "Usuário selecionado não encontrado."
            queryset = Usuario.objects.filter(is_active=True).prefetch_related('groups').order_by('username')
            paginador = Paginator(queryset, 20)
            page_obj = paginador.get_page(request.GET.get('page'))
            contexto['page_obj'] = page_obj
            return render(request, 'ativos/chaves/entregar_chave.html', contexto)

        # Registro de aquisição pelo usuário selecionado
        HistoricoEmprestimo.objects.create(
            chave=chave,
            usuario=usuario_selecionado,
            acao='adquirida'
        )

        return redirect(request.GET.get('next', 'lista_chaves'))

    # GET: busca e lista usuários com indicação de permissão por grupo
    else:
        busca_termo = request.GET.get('busca_usuario', '')

        queryset = Usuario.objects.filter(is_active=True).prefetch_related('groups').order_by('username')

        if busca_termo:
            queryset = queryset.filter(
                Q(username__icontains=busca_termo) |
                Q(first_name__icontains=busca_termo) |
                Q(last_name__icontains=busca_termo)
            )

        paginador = Paginator(queryset, 20)
        pagina_num = request.GET.get('page')
        page_obj = paginador.get_page(pagina_num)

        # Grupos exigidos pela chave
        grupos_requeridos_ids = set(chave.grupos_permissao.values_list('pk', flat=True))
        nomes_grupos = ", ".join(g.name for g in chave.grupos_permissao.all())

        # Marca flag de permissão por usuário (para o template)
        if not grupos_requeridos_ids:
            for usuario in page_obj.object_list:
                usuario.tem_permissao = True
        else:
            for usuario in page_obj.object_list:
                grupos_usuario_ids = set(usuario.groups.values_list('pk', flat=True))
                usuario.tem_permissao = not grupos_requeridos_ids.isdisjoint(grupos_usuario_ids)

        contexto['page_obj'] = page_obj
        contexto['busca_termo'] = busca_termo
        contexto['nomes_grupos_requeridos'] = nomes_grupos
        return render(request, 'ativos/chaves/entregar_chave.html', contexto)
