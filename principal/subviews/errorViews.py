# Author: João Victor Marques Favero
from django.shortcuts import render

def custom_page_not_found_view(request, exception):
    """
    View customizada para renderizar a página 404.
    """
    # Renderiza o template de erro 404
    return render(request, 'error/404.html', status=404)