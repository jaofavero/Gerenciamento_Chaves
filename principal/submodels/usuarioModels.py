from django.db import models
from django.contrib.auth.models import AbstractUser, Group

class Usuario(AbstractUser):
    """
    Modelo de Usuário customizado que estende o User padrão do Django.
    Isso nos permite adicionar campos específicos da instituição (como CPF e contato)
    enquanto mantemos toda a integração com o sistema de autenticação e permissões.
    """
    # Campo para armazenar o CPF do usuário, deve ser único
    cpf = models.CharField('CPF', max_length=15, unique=True, help_text='CPF do servidor.')
    
    # Campo para armazenar o telefone de contato do usuário
    contato = models.CharField('Contato', max_length=15, help_text='Telefone de contato do servidor.')
    
    # Relacionamento many-to-many com grupos
    # Sobrescrito para evitar conflitos com o modelo User padrão do Django
    groups = models.ManyToManyField(
        Group,
        verbose_name='grupos',
        blank=True,
        help_text='Os grupos a que este usuário pertence. Um usuário terá todas as permissões concedidas a cada um dos seus grupos.',
        related_name="usuario_set",    # Nome personalizado para a relação reversa
        related_query_name="usuario",  # Nome para consultas reversas
    )

    # Relacionamento many-to-many com permissões
    # Sobrescrito para evitar conflitos com o modelo User padrão do Django
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='permissões do usuário',
        blank=True,
        help_text='Permissões específicas para este usuário.',
        related_name="usuario_set",    # Nome personalizado para a relação reversa
        related_query_name="usuario",  # Nome para consultas reversas
    )

    # Método que retorna a representação em string do usuário
    # Retorna o nome completo se existir, senão retorna o username
    def __str__(self):
        return self.get_full_name() or self.username