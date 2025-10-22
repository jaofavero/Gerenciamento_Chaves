from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from principal.models import HistoricoEmprestimo, Chave, Usuario

from .subviews.chaveViews import lista_chaves, pegar_chave, receber_chave, entregar_chave
from .subviews.emprestimoViews import historico_list, api_ultimos_emprestimos
from .subviews.indexViews import index