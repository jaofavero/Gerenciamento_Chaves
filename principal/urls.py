# Author: João Victor Marques Favero
"""
Arquivo de configuração de URLs do aplicativo 'principal'.

- Define as rotas (paths) que mapeiam URLs para as views correspondentes.
- Inclui URLs de apps externos (ex.: 'qr_code').
- Configura autenticação (login/logout) usando as views padrão do Django.
- Define um handler customizado para erros 404.
"""

from django.urls import include, path  # path: define rotas; include: inclui URLs de outro app
from . import views  # importa as views locais do app 'principal'
from django.contrib.auth import views as auth_views  # views de autenticação (login/logout) do Django

# Lista de URLs do aplicativo principal
urlpatterns = [
    # URL: / (Raiz)
    # View: views.index
    # Nome: 'index' (usado em {% url 'index' %})
    path('', views.index, name='index'),

    # URL: /qr_code/
    # Inclui as URLs do app 'qr_code' com namespace 'qr_code' (evita conflitos de nomes)
    path('qr_code/', include('qr_code.urls', namespace='qr_code')),

    # URL: /scan/
    # View: views.scan_page (página para leitura/scanner de QR Code)
    # Nome: 'scan_page'
    path('scan/', views.scan_page, name='scan_page'),

    # URL: /historico/
    # View: views.historico_list
    # Nome: 'historico_list'
    path('historico/', views.historico_list, name='historico_list'),
    
    # URL: /api/ultimos-emprestimos/
    # View: views.api_ultimos_emprestimos
    # Nome: 'api_ultimos_emprestimos'
    path('api/ultimos-emprestimos/', views.api_ultimos_emprestimos, name='api_ultimos_emprestimos'),
    
    # URL: /chave/1/ (ou /chave/2/, etc.)
    # View: views.pegar_chave
    # Nome: 'pegar_chave' (usado em {% url 'pegar_chave' pk=chave.pk %})
    path('chave/<int:pk>/', views.pegar_chave, name='pegar_chave'),

    # URL: /chaves/
    # View: views.lista_chaves
    # Nome: 'lista_chaves' (usado em {% url 'lista_chaves' %})
    path('chaves/', views.lista_chaves, name='lista_chaves'),

    # URL: /chave/<pk>/receber/
    # View: views.receber_chave (processa a devolução/recebimento de uma chave)
    # Nome: 'receber_chave'
    path('chave/<int:pk>/receber/', views.receber_chave, name='receber_chave'),
    
    # URL: /chave/<pk>/entregar/
    # View: views.entregar_chave (entrega/associa a chave a um usuário)
    # Nome: 'entregar_chave'
    path('chave/<int:pk>/entregar/', views.entregar_chave, name='entregar_chave'),

    # URL: /chave/<pk>/qrcode/
    # View: views.gerar_qrcode_chave (gera o QR Code da chave especificada)
    # Nome: 'gerar_qrcode_chave'
    path('chave/<int:pk>/qrcode/', views.gerar_qrcode_chave, name='gerar_qrcode_chave'),

    # URL: /login/
    # View: auth_views.LoginView (com template 'usuario/login.html')
    # Nome: 'login' (usado em {% url 'login' %})
    path('login/', auth_views.LoginView.as_view(template_name='usuario/login.html'), name='login'),
    
    # URL: /logout/
    # View: auth_views.LogoutView (encerra a sessão do usuário autenticado)
    # Nome: 'logout' (usado em {% url 'logout' %})
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

# Handler customizado para páginas não encontradas (HTTP 404)
# Aponta para a view 'custom_page_not_found_view' dentro de 'principal.views'
handler404 = 'principal.views.custom_page_not_found_view'