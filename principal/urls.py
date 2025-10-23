from django.urls import include, path
from . import views
from django.contrib.auth import views as auth_views

# Lista de URLs do aplicativo principal
urlpatterns = [
    # URL: / (Raiz)
    # View: views.index
    # Nome: 'index' (usado em {% url 'index' %})
    path('', views.index, name='index'),

    path('qr_code/', include('qr_code.urls', namespace='qr_code')),

    path('scan/', views.scan_page, name='scan_page'),

    # URL: /historico/
    # View: views.historico_list
    # Nome: 'historico_list'
    path('historico/', views.historico_list, name='historico_list'),
    
    # URL: /api/ultimos-emprestimos/
    # View: views.api_ultimos_emprestimos
    # Nome: 'api_ultimos_emprestimos'
    # Esta é a URL que o nosso JavaScript vai chamar
    path('api/ultimos-emprestimos/', views.api_ultimos_emprestimos, name='api_ultimos_emprestimos'),
    
    # URL: /chave/1/ (ou /chave/2/, etc.)
    # View: views.pegar_chave
    # Nome: 'pegar_chave' (usado em {% url 'pegar_chave' pk=chave.pk %})
    path('chave/<int:pk>/', views.pegar_chave, name='pegar_chave'),

    # URL: /chaves/
    # View: views.lista_chaves
    # Nome: 'lista_chaves' (usado em {% url 'lista_chaves' %})
    path('chaves/', views.lista_chaves, name='lista_chaves'),

    path('chave/<int:pk>/receber/', views.receber_chave, name='receber_chave'),
    
    # URL para a página de "Entregar" uma chave para um usuário
    path('chave/<int:pk>/entregar/', views.entregar_chave, name='entregar_chave'),

    path('chave/<int:pk>/qrcode/', views.gerar_qrcode_chave, name='gerar_qrcode_chave'),

    # URL: /login/
    # View: auth_views.LoginView (com template 'usuario/login.html')
    # Nome: 'login' (usado em {% url 'login' %})
    path('login/', auth_views.LoginView.as_view(template_name='usuario/login.html'), name='login'),
    
    # URL: /logout/
    # View: auth_views.LogoutView
    # Nome: 'logout' (usado em {% url 'logout' %})
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

handler404 = 'principal.views.custom_page_not_found_view'