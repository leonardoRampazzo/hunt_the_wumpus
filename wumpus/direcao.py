from enum import *

class Direcao(Enum):
    NORTE = (0, 1)
    LESTE = (1, 0)
    OESTE = (-1, 0)
    SUL = (0, -1)

    def __init__(self, x, y):
        self.ponto = (x, y)

    def validacao_rotacao_90(self, direcao):
        if direcao in [Direcao.NORTE, Direcao.SUL]:
            return self in [Direcao.LESTE, Direcao.OESTE]

        return self in [Direcao.NORTE, Direcao.SUL]