from enum import *

class AcaoAgente(Enum):
    ANDAR = auto()
    RODAR_DIREITA = auto()
    RODAR_ESQUERDA = auto()
    PEGAR_OURO = auto()
    MATAR_WUMPUS = auto()