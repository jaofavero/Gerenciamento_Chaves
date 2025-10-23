# Author: João Victor Marques Favero
"""
Modelo Chave para gerenciamento de chaves físicas.
"""

from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from .usuarioModels import Usuario

class Chave(models.Model):
    """
    Representa uma chave física controlada pelo sistema.
    """

    # Opções de status
    STATUS_CHOICES = [
        ('disponivel', 'Disponível'),
        ('em_uso', 'Em Uso'),
    ]

    # Nome único da chave
    nome = models.CharField(
        'Nome da Chave',
        max_length=100,
        unique=True,
        help_text='Ex: Laboratório de Redes, Sala 203.'
    )

    # Descrição opcional
    descricao = models.TextField(
        'Descrição',
        blank=True,
        help_text='Informações adicionais sobre a chave ou o local.'
    )

    # Status atual (default: disponível)
    status = models.CharField(
        'Status Atual',
        max_length=20,
        choices=STATUS_CHOICES,
        default='disponivel'
    )

    # Usuário que está com a chave (pode ser nulo)
    portador_atual = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='chaves_em_posse',
        verbose_name='Portador Atual'
    )

    # Grupos com permissão para retirar (vazio = qualquer autenticado)
    grupos_permissao = models.ManyToManyField(
        Group,
        blank=True,
        verbose_name='Grupo com Permissão',
        help_text='Se definido, apenas usuários deste grupo podem retirar esta chave.'
    )

    # Exclusão lógica (soft delete)
    excluido = models.BooleanField(
        'Excluído (Logicamente)',
        default=False,
        help_text='Não aparece para novos empréstimos, mas mantém histórico.'
    )

    class Meta:
        verbose_name = 'Chave'
        verbose_name_plural = 'Chaves'

    def __str__(self):
        # Exibe o nome da chave
        return self.nome
