from django.db import models
from django.contrib.auth.models import AbstractUser, Group

class Usuario(AbstractUser):
    """
    Modelo de Usuário customizado que estende o User padrão do Django.
    Isso nos permite adicionar campos específicos da instituição (como CPF e contato)
    enquanto mantemos toda a integração com o sistema de autenticação e permissões.
    """
    cpf = models.CharField('CPF', max_length=15, unique=True, help_text='CPF do servidor.')
    contato = models.CharField('Contato', max_length=15, help_text='Telefone de contato do servidor.')
    
    # Adicionar related_name para evitar conflitos com o User padrão do Django
    groups = models.ManyToManyField(
        Group,
        verbose_name='grupos',
        blank=True,
        help_text='Os grupos a que este usuário pertence. Um usuário terá todas as permissões concedidas a cada um dos seus grupos.',
        related_name="usuario_set",
        related_query_name="usuario",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='permissões do usuário',
        blank=True,
        help_text='Permissões específicas para este usuário.',
        related_name="usuario_set",
        related_query_name="usuario",
    )

    def __str__(self):
        return self.get_full_name() or self.username