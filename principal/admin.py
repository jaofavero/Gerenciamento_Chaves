# Author: João Victor Marques Favero

from django.contrib import admin  # Admin do Django
from django.contrib.auth.admin import UserAdmin  # Admin padrão de usuários
from principal.models import Usuario, Chave, HistoricoEmprestimo  # Modelos do app

# Admin customizado para o modelo de usuário
class UsuarioAdmin(UserAdmin):
    # Inclui 'cpf' e 'contato' nas seções de edição do usuário
    fieldsets = UserAdmin.fieldsets + (
        ('Informações Customizadas', {'fields': ('cpf', 'contato')}),
    )

    # Campos exibidos ao criar um novo usuário (inclui nome/sobrenome/email, customizados e grupos)
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('first_name', 'last_name', 'email')}),
        ('Informações Customizadas', {'fields': ('cpf', 'contato')}),
        ('Permissões', {'fields': ('groups',)}),
    )

    # Mostra contato e cpf na lista de usuários
    list_display = UserAdmin.list_display + ('contato', 'cpf')

# Admin para o modelo Chave
class ChaveAdmin(admin.ModelAdmin):
    # Colunas exibidas na lista de chaves
    list_display = ('nome', 'status', 'portador_atual', 'excluido')
    # Widget horizontal para ManyToMany de grupos de permissão
    filter_horizontal = ('grupos_permissao',)

# Admin para o histórico de empréstimos
class HistoricoEmprestimoAdmin(admin.ModelAdmin):
    # Colunas exibidas na lista de históricos
    list_display = ('chave', 'usuario', 'data_hora', 'acao')

# Registros no site de administração
admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Chave, ChaveAdmin)
admin.site.register(HistoricoEmprestimo, HistoricoEmprestimoAdmin)