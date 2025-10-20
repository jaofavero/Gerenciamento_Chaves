from django.urls import path
from . import views

# Lista de URLs do aplicativo principal
urlpatterns = [
    # URL: / (Raiz)
    # View: views.index
    # Nome: 'index' (usado em {% url 'index' %})
    path('', views.index, name='index'),
    
    # URL: /historico/
    # View: views.historico_list
    # Nome: 'historico_list'
    path('historico/', views.historico_list, name='historico_list'),
    
    # URL: /api/ultimos-emprestimos/
    # View: views.api_ultimos_emprestimos
    # Nome: 'api_ultimos_emprestimos'
    # Esta é a URL que o nosso JavaScript vai chamar
    path('api/ultimos-emprestimos/', views.api_ultimos_emprestimos, name='api_ultimos_emprestimos'),
]