# Imports necessários para esta view
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from principal.models import Chave # Importa o modelo Chave

@login_required
def gerar_qrcode_chave(request, pk):
    """
    View para exibir um QR Code para uma chave específica, usando django-qr-code.
    """
    # 1. Garante que apenas staff possa acessar
    if not request.user.is_staff:
        return redirect('index')

    # 2. Busca a chave
    chave = get_object_or_404(Chave, pk=pk)

    # 3. Constrói a URL que o QR Code deve conter
    # request.build_absolute_uri() cria a URL completa (ex: http://localhost:8000/chave/1/)
    url_chave = request.build_absolute_uri(reverse('pegar_chave', args=[chave.pk]))
    
    # 4. Passa a URL para o template
    contexto = {
        'chave': chave,
        'url_para_qrcode': url_chave
    }
    
    # 5. Renderiza o template que criamos anteriormente
    return render(request, 'ativos/qrcode/qrcode_chave.html', contexto)