from wumpus.acao_agente import AcaoAgente
from wumpus.direcao import Direcao
import wumpus.ponto as wp
import operator


class RotacaoDirecaoInvalida(Exception):
    def __init__(self, direcao_atual, direcao_nova):
        super(RotacaoDirecaoInvalida, self).__init__(
            "Rotação de posição atual é invalida!")


class Posicao:
    def __init__(self, ponto, direcao):
        self._ponto = ponto
        self._direcao = direcao
       
    def __str__(self):
        return "({}, {})".format(str(self._ponto), self._direcao)

    def __repr__(self):
        return "Posicao({}, {})".format(str(self._ponto), self._direcao)

    def adjacentes(self):
        return wp.calcular_adjacentes(self.ponto())

    def rodar(self, direcao):
        if self._direcao.validacao_rotacao_90(direcao):
            return Posicao(
                self._ponto,
                direcao
            )
        else:
            raise RotacaoDirecaoInvalida(self._direcao, self.direcao)

    def andar(self):
        return Posicao(
            wp.somar_pontos(self._ponto, self._direcao.value),
            self._direcao
        )

    def ponto(self):
        return self._ponto

    def direcao(self):
        return self._direcao    

    def calcular_posicao(self, acao):
        if acao == AcaoAgente.ANDAR:
            return self.andar()
        else:
            if self.direcao() == Direcao.NORTE:
                if acao == AcaoAgente.RODAR_DIREITA:
                    return self.rodar(Direcao.LESTE)
                else:
                    return self.rodar(Direcao.OESTE)
            if self.direcao() == Direcao.SUL:
                if acao == AcaoAgente.RODAR_DIREITA:
                    return self.rodar(Direcao.OESTE)
                else:
                    return self.rodar(Direcao.LESTE)
            if self.direcao() == Direcao.LESTE:
                if acao == AcaoAgente.RODAR_DIREITA:
                    return self.rodar(Direcao.SUL)
                else:
                    return self.rodar(Direcao.NORTE)
            if self.direcao() == Direcao.OESTE:
                if acao == AcaoAgente.RODAR_DIREITA:
                    return self.rodar(Direcao.NORTE)
                else:
                    return self.rodar(Direcao.SUL)

        return self
