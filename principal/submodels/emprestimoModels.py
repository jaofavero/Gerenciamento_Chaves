# Author: João Victor Marques Favero

from django.db import models
from django.contrib.auth.models import AbstractUser
from ..submodels.usuarioModels import Usuario
from .chaveModels import Chave

class HistoricoEmprestimo(models.Model):
    # Tipos de ação registrados no histórico
    ACAO_CHOICES = [
        ('adquirida', 'Adquirida'),
        ('devolucao', 'Devolução'),
        ('transferida', 'Transferida'),
    ]

    # Chave movimentada (SET_NULL preserva histórico se a chave for excluída)
    chave = models.ForeignKey(
        Chave,
        on_delete=models.SET_NULL,
        null=True,
        related_name='historico',
        verbose_name='Chave Transacionada'
    )
    
    # Usuário responsável (SET_NULL preserva registro se o usuário for excluído)
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Usuário Responsável'
    )
    
    # Data/hora automática da ação
    data_hora = models.DateTimeField('Data e Hora da Ação', auto_now_add=True)
    
    # Tipo da ação
    acao = models.CharField('Ação Realizada', max_length=20, choices=ACAO_CHOICES)

    class Meta:
        verbose_name = 'Histórico de Empréstimo'
        verbose_name_plural = 'Históricos de Empréstimos'
        ordering = ['-data_hora']  # Mais recente primeiro

    def save(self, *args, **kwargs):
        """
        Aplica regras de negócio ao criar um novo histórico (aquisição/devolução/transferência).
        """
        is_new = self.pk is None  # Executa apenas na criação

        if is_new:
            if self.acao == 'adquirida':
                # Chave sendo movimentada
                chave_movimentada = self.chave
                # Portador anterior, se houver
                portador_anterior = chave_movimentada.portador_atual

                # Se havia portador e é diferente do novo usuário, registra transferência
                if portador_anterior is not None and portador_anterior != self.usuario:
                    HistoricoEmprestimo.objects.create(
                        chave=chave_movimentada,
                        usuario=portador_anterior,
                        acao='transferida'
                    )

                # Atualiza status e portador atual da chave
                chave_movimentada.status = 'em_uso'
                chave_movimentada.portador_atual = self.usuario
                chave_movimentada.save()

            elif self.acao == 'devolucao':
                # Devolução para a portaria: chave volta a ficar disponível
                self.chave.status = 'disponivel'
                self.chave.portador_atual = None
                self.chave.save()

        super().save(*args, **kwargs)

    def __str__(self):
        # Resiliente a chaves/usuários excluídos
        nome_chave = self.chave.nome if self.chave else "[Chave Excluída]"
        nome_usuario = self.usuario.username if self.usuario else "[Usuário Excluído]"
        data_formatada = self.data_hora.strftime("%d/%m/%Y às %H:%M")
        return f'{nome_chave} - {self.get_acao_display()} por {nome_usuario} em {data_formatada}'
