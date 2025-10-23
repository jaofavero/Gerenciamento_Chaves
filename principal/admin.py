from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from principal.models import Usuario, Chave, HistoricoEmprestimo

# Register your models here.
class UsuarioAdmin(UserAdmin):
    
    # Adiciona os campos 'cpf' e 'contato' aos 'fieldsets' 
    fieldsets = UserAdmin.fieldsets + (
        ('Informações Customizadas', {'fields': ('cpf', 'contato')}),
    )

    # Adiciona os campos 'cpf' e 'contato' ao 'add_fieldsets'
    # (os campos exibidos ao CRIAR um novo usuário).
    add_fieldsets = UserAdmin.add_fieldsets + (
        # Adiciona Nome, Sobrenome e Email à primeira seção padrão
        (None, {'fields': ('first_name', 'last_name', 'email')}), 
        # Adiciona a seção de Informações Customizadas
        ('Informações Customizadas', {'fields': ('cpf', 'contato')}),
        # Adiciona Grupos à seção de Permissões padrão
        ('Permissões', {'fields': ('groups',)}), 
    )
            


    list_display = UserAdmin.list_display + ('contato', 'cpf')

class ChaveAdmin(admin.ModelAdmin):
    list_display = ('nome', 'status', 'portador_atual', 'excluido')
    filter_horizontal = ('grupos_permissao',)


class HistoricoEmprestimoAdmin(admin.ModelAdmin):
    list_display = ('chave', 'usuario', 'data_hora', 'acao')

admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Chave, ChaveAdmin)
admin.site.register(HistoricoEmprestimo, HistoricoEmprestimoAdmin)