from wumpus.percepcao_ambiente import PercepcaoAmbiente
import wumpus.ponto as wp


class PontoInvalidoGeracaoAmbiente(Exception):
    pass


class AmbienteWumpus:
    def __init__(self, limite):
        self.__limite = limite
        self.__wumpus = []
        self.__ouro = self.__limite
        self.__pocos = []

    def __ponto_adjacente__(self, ponto, ponto2):
        adjacentes = wp.calcular_adjacentes_limitados(ponto, self.__limite)
        return (ponto2 in adjacentes)

    def fedor(self, ponto):
        for ponto_wumpus in self.__wumpus:
            if self.__ponto_adjacente__(ponto, ponto_wumpus):
                return True

        return False

    def brisa(self, ponto):
        for ponto_poco in self.__pocos:
            if self.__ponto_adjacente__(ponto, ponto_poco):
                return True

        return False

    def add_wumpus(self, ponto):
        if ponto == (1, 1):
            raise PontoInvalidoGeracaoAmbiente()

        self.__wumpus.append(ponto)

    def add_poco(self, ponto):
        if ponto == (1, 1):
            raise PontoInvalidoGeracaoAmbiente()

        self.__pocos.append(ponto)

    def add_ouro(self, ponto):
        if ponto == (1, 1):
            raise PontoInvalidoGeracaoAmbiente()

        self.__ouro = ponto

    def percepcao(self, ponto):
        return {
            PercepcaoAmbiente.FEDOR: self.fedor(ponto),
            PercepcaoAmbiente.BRISA: self.brisa(ponto),
            PercepcaoAmbiente.BRILHO: self.__ouro == ponto,
            PercepcaoAmbiente.GRITO: not self.__wumpus,
        }

    def limite(self):
        return self.__limite

    def pegar_ouro(self, ponto):
        if self.ouro(ponto):
            self.__ouro = (0, 0)

    def atirar_flecha(self, posicao):
        ponto = posicao.ponto()
        direcao = posicao.direcao()
        x, y = ponto
        while (wp.dentro_limite(ponto, self.__limite)):
            ponto = wp.somar_pontos(ponto, direcao.value)
            if self.wumpus(ponto):
                self.__wumpus.remove(ponto)

    def poco(self, ponto):
        return ponto in self.__pocos

    def wumpus(self, ponto):
        return ponto in self.__wumpus

    def ouro(self, ponto):
        return ponto == self.__ouro
