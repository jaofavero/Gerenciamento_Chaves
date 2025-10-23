from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from .usuarioModels import Usuario

class Chave(models.Model):
    """
    Representa um ativo físico (uma chave) a ser gerenciado pelo sistema.
    """
    # Define as opções de status possíveis para uma chave
    STATUS_CHOICES = [
        ('disponivel', 'Disponível'),
        ('em_uso', 'Em Uso'),
    ]

    # Campo para o nome da chave, deve ser único
    nome = models.CharField('Nome da Chave', max_length=100, unique=True, help_text='Ex: Laboratório de Redes, Sala 203.')
    
    # Campo opcional para descrição detalhada da chave
    descricao = models.TextField('Descrição', blank=True, help_text='Informações adicionais sobre a chave ou o local.')
    
    # Campo para controle do status atual da chave
    status = models.CharField(
        'Status Atual',
        max_length=20,
        choices=STATUS_CHOICES,
        default='disponivel'
    )
    
    # Relacionamento com o usuário que está atualmente com a chave
    portador_atual = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='chaves_em_posse',
        verbose_name='Portador Atual'
    )
    
    # Grupo de usuários que tem permissão para retirar a chave
    grupos_permissao = models.ManyToManyField(
        Group,
        null=True,
        blank=True,
        verbose_name='Grupo com Permissão',
        help_text='Se definido, apenas usuários deste grupo podem retirar esta chave.'
    )
    excluido = models.BooleanField(
        'Excluído (Logicamente)',
        default=False,
        help_text='Se marcado, a chave não aparecerá para novos empréstimos, mas será mantida no histórico.'
    )
    class Meta:
        verbose_name = 'Chave'
        verbose_name_plural = 'Chaves'

    def __str__(self):
        return self.nome
    
