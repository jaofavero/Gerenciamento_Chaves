from django.db import models

# Create your models here.
# Models são como classes que definem a estrutura dos dados que serão armazenados no banco de dados.

#import submodels
from .submodels.usuarioModels import Usuario
from .submodels.chaveModels import Chave
from .submodels.emprestimoModels import HistoricoEmprestimo
