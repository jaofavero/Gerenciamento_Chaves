# Imports para todas as funções neste arquivo
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from principal.models import Chave # Importa o modelo Chave

# Imports para a função de scan (upload)
from django.contrib import messages
from PIL import Image
from pyzbar.pyzbar import decode


@login_required
def gerar_qrcode_chave(request, pk):
    """
    View para exibir um QR Code para uma chave específica (usando django-qr-code).
    """
    # 1. Garante que apenas staff possa acessar
    if not request.user.is_staff:
        return redirect('index')

    # 2. Busca a chave
    chave = get_object_or_404(Chave, pk=pk)

    # 3. Constrói a URL que o QR Code deve conter
    url_chave = request.build_absolute_uri(reverse('pegar_chave', args=[chave.pk]))
    
    # 4. Passa a URL para o template
    contexto = {
        'chave': chave,
        'url_para_qrcode': url_chave
    }
    
    # 5. Renderiza o template que exibe o QR Code
    return render(request, 'ativos/qrcode/qrcode_chave.html', contexto)


@login_required
def scan_page(request):
    """
    View para a página de upload e processamento do QR Code (usando pyzbar).
    """
    if request.method == 'POST':
        # 1. Verifica se um arquivo foi enviado
        if 'qr_image' not in request.FILES:
            messages.error(request, 'Nenhum arquivo enviado.')
            return redirect('index') # <- ALTERADO DE 'scan_page' PARA 'index'

        image_file = request.FILES['qr_image']

        try:
            # 2. Abre a imagem
            img = Image.open(image_file)
            
            # 3. Decodifica a imagem
            decoded_objects = decode(img)

            if decoded_objects:
                # 4. Pega o link e redireciona (SUCESSO)
                url = decoded_objects[0].data.decode('utf-8')
                return redirect(url)
            else:
                messages.error(request, 'Nenhum QR Code encontrado na imagem. Tente novamente.')
                return redirect('index') # <- ALTERADO DE 'scan_page' PARA 'index'
                
        except Exception as e:
            messages.error(request, f'Erro ao processar a imagem: {e}')
            return redirect('index') # <- ALTERADO DE 'scan_page' PARA 'index'

    else:
        # Método GET: Se o usuário for para /scan/ manualmente,
        # ele ainda vê a página de scan dedicada.
        return render(request, 'ativos/qrcode/scan_page.html')