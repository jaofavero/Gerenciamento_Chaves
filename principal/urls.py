from django.urls import path
from . import views

#Lista de URLs do aplicativo principal
urlpatterns = [
    path('', views.index, name='index'),
]