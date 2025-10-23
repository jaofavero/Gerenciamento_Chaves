# Author: João Victor Marques Favero

from django.db import models
from django.contrib.auth.models import AbstractUser, Group

class Usuario(AbstractUser):
    """
    Usuário customizado com CPF e contato; mantém autenticação/permissões do Django.
    """
    # CPF único do servidor
    cpf = models.CharField('CPF', max_length=15, unique=True, help_text='CPF do servidor.')
    # Telefone de contato
    contato = models.CharField('Contato', max_length=15, help_text='Telefone de contato do servidor.')
    
    # Grupos (M2M) com nomes reversos personalizados para evitar conflito com User padrão
    groups = models.ManyToManyField(
        Group,
        verbose_name='grupos',
        blank=True,
        help_text='Os grupos a que este usuário pertence. Um usuário terá todas as permissões concedidas a cada um dos seus grupos.',
        related_name="usuario_set",
        related_query_name="usuario",
    )

    # Permissões (M2M) com nomes reversos personalizados
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='permissões do usuário',
        blank=True,
        help_text='Permissões específicas para este usuário.',
        related_name="usuario_set",
        related_query_name="usuario",
    )

    # Retorna nome completo; se ausente, retorna username
    def __str__(self):
        return self.get_full_name() or self.username
