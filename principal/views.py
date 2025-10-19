from django.shortcuts import render
from django.http import HttpResponse
from principal.models import HistoricoEmprestimo
# Create your views here.
def index(request):
    emprestimos = HistoricoEmprestimo.objects.all()
    emprestimosDicionario = {'emprestimos': emprestimos}
    return render(request, 'emprestimos/index.html', emprestimosDicionario)