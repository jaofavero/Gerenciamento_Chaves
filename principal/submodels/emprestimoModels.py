# Importações necessárias
from django.db import models
from django.contrib.auth.models import AbstractUser
from ..submodels.usuarioModels import Usuario
from .chaveModels import Chave

class HistoricoEmprestimo(models.Model):

    # Define as opções possíveis para o campo 'acao'
    ACAO_CHOICES = [
        ('adquirida', 'Adquirida'),
        ('devolucao', 'Devolução'),
        ('transferida', 'Transferida'),
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

    def save(self, *args, **kwargs):
            """
            Sobrescreve o método save() com a nova lógica de transferência.
            """
            # Só executamos esta lógica na CRIAÇÃO de um novo registro
            is_new = self.pk is None

            if is_new:
                if self.acao == 'adquirida':
                    # Identificando a chave que está a ser movimentada
                    chave_movimentada = self.chave
                    
                    # Verificando quem era o portador anterior
                    portador_anterior = chave_movimentada.portador_atual

                    if portador_anterior is not None and portador_anterior != self.usuario:
                        
                        HistoricoEmprestimo.objects.create(
                            chave=chave_movimentada,
                            usuario=portador_anterior, # O usuário que ESTAVA com a chave
                            acao='transferida'
                        )

                    chave_movimentada.status = 'em_uso'
                    chave_movimentada.portador_atual = self.usuario # O usuário que ADQUIRIU
                    chave_movimentada.save()
                #Devolução significa quando a chave é devolvida para a portaria
                elif self.acao == 'devolucao':
                    # Atualiza a chave relacionada
                    self.chave.status = 'disponivel'
                    self.chave.portador_atual = None # Remove o portador
                    self.chave.save() # Salva a chave com o novo status

            super().save(*args, **kwargs)

    def __str__(self):
            # Método __str__ robusto que funciona mesmo se a chave ou usuário forem nulos
            nome_chave = self.chave.nome if self.chave else "[Chave Excluída]"
            nome_usuario = self.usuario.username if self.usuario else "[Usuário Excluído]"
            data_formatada = self.data_hora.strftime("%d/%m/%Y às %H:%M")
            
            return f'{nome_chave} - {self.get_acao_display()} por {nome_usuario} em {data_formatada}'