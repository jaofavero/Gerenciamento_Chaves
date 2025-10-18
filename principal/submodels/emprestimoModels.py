# Importações necessárias
from django.db import models
from django.contrib.auth.models import AbstractUser
from ..submodels.usuarioModels import Usuario
from .chaveModels import Chave

class HistoricoEmprestimo(models.Model):
    """
    Modelo que funciona como um log de auditoria, registrando todas as
    operações de retirada e devolução de chaves.
    """
    # Define as opções possíveis para o campo 'acao'
    ACAO_CHOICES = [
        ('retirada', 'Retirada'),
        ('devolucao', 'Devolução'),
    ]

    # Relacionamento com o modelo Chave
    # CASCADE: se a chave for deletada, deleta também os registros históricos
    chave = models.ForeignKey(
        Chave,
        on_delete=models.SET_NULL, # Preserva o histórico se a chave for deletada
        null=True, # Permite que o campo 'chave' fique nulo
        related_name='historico',
        verbose_name='Chave Transacionada'
    )
    
    # Relacionamento com o modelo Usuario
    # SET_NULL: se o usuário for deletado, mantém o registro mas sem referência ao usuário
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Usuário Responsável'
    )
    
    # Campo automático que registra a data e hora da ação
    data_hora = models.DateTimeField('Data e Hora da Ação', auto_now_add=True)
    
    # Campo que armazena o tipo de ação (retirada ou devolução)
    acao = models.CharField('Ação Realizada', max_length=20, choices=ACAO_CHOICES)

    class Meta:
        # Define configurações do modelo
        verbose_name = 'Histórico de Empréstimo'
        verbose_name_plural = 'Históricos de Empréstimos'
        ordering = ['-data_hora']  # Ordena do mais recente para o mais antigo

def __str__(self):
        # Método __str__ robusto que funciona mesmo se a chave ou usuário forem nulos
        nome_chave = self.chave.nome if self.chave else "[Chave Excluída]"
        nome_usuario = self.usuario.username if self.usuario else "[Usuário Excluído]"
        data_formatada = self.data_hora.strftime("%d/%m/%Y às %H:%M")
        
        return f'{nome_chave} - {self.get_acao_display()} por {nome_usuario} em {data_formatada}'