from django.shortcuts import render

def custom_page_not_found_view(request, exception):
    """
    View customizada para renderizar a página 404.
    """
    # Aponta para o novo caminho do template
    return render(request, 'error/404.html', status=404)