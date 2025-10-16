from django.db import models
from django.contrib.auth.models import AbstractUser
from ..submodels.usuarioModels import Usuario
from ..submodels.ativoModels import Chave

class HistoricoEmprestimo(models.Model):
    """
    Modelo que funciona como um log de auditoria, registrando todas as
    operações de retirada e devolução de chaves.
    """
    ACAO_CHOICES = [
        ('retirada', 'Retirada'),
        ('devolucao', 'Devolução'),
    ]

    chave = models.ForeignKey(
        Chave,
        on_delete=models.CASCADE,
        related_name='historico',
        verbose_name='Chave Transacionada'
    )
    
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL, # Mantém o histórico mesmo se o usuário for removido
        null=True,
        verbose_name='Usuário Responsável'
    )
    
    data_hora = models.DateTimeField('Data e Hora da Ação', auto_now_add=True)
    
    acao = models.CharField('Ação Realizada', max_length=20, choices=ACAO_CHOICES)

    class Meta:
        verbose_name = 'Histórico de Empréstimo'
        verbose_name_plural = 'Históricos de Empréstimos'
        ordering = ['-data_hora'] # Ordena os registros mais recentes primeiro

    def __str__(self):
        return f'{self.chave.nome} - {self.get_acao_display()} por {self.usuario.username} em {self.data_hora.strftime("%d/%m/%Y %H:%M")}'