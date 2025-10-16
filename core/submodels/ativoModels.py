from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from ..submodels.usuarioModels import Usuario

class Chave(models.Model):
    """
    Representa um ativo físico (uma chave) a ser gerenciado pelo sistema.
    """
    STATUS_CHOICES = [
        ('disponivel', 'Disponível'),
        ('em_uso', 'Em Uso'),
    ]

    nome = models.CharField('Nome da Chave', max_length=100, unique=True, help_text='Ex: Laboratório de Redes, Sala 203.')
    descricao = models.TextField('Descrição', blank=True, help_text='Informações adicionais sobre a chave ou o local.')
    
    status = models.CharField(
        'Status Atual',
        max_length=20,
        choices=STATUS_CHOICES,
        default='disponivel'
    )
    
    portador_atual = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='chaves_em_posse',
        verbose_name='Portador Atual'
    )
    
    grupo_permissao = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Grupo com Permissão',
        help_text='Se definido, apenas usuários deste grupo podem retirar esta chave.'
    )

    class Meta:
        verbose_name = 'Chave'
        verbose_name_plural = 'Chaves'

    def __str__(self):
        return self.nome