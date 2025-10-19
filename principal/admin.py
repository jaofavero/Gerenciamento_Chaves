from django.contrib import admin
from principal.models import Usuario, Chave, HistoricoEmprestimo

# Register your models here.
class UsuarioAdmin(admin.ModelAdmin):
    #Estamon aproveitando de uma funcionalidade do Django para o usuario, por esse motivo usamos "username" e "email"
    list_display = ('username', 'email', 'contato', 'cpf')
    '''user_permissions', 'groups'''

class ChaveAdmin(admin.ModelAdmin):
    list_display = ('nome', 'status', 'portador_atual', 'grupo_permissao', 'excluido')

class HistoricoEmprestimoAdmin(admin.ModelAdmin):
    list_display = ('chave', 'usuario', 'data_hora', 'acao')

admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Chave, ChaveAdmin)
admin.site.register(HistoricoEmprestimo, HistoricoEmprestimoAdmin)