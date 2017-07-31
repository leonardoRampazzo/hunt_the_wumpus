from wumpus.base_dados import BaseDadosAgente
import wumpus.ponto as wp
import os
import abc


@BaseDadosAgente.register
class BaseDadosAgentePython:
    def __init__(self):
        self.__fedor = []
        self.__brisa = []
        self.__visitados = set([])
        self.__limite = (4, 4)

    def tell_visitado(self, ponto):
        self.__visitados.add(ponto)

    def tell_fedor(self, ponto):
        self.__fedor.append(ponto)

    def tell_brisa(self, ponto):
        self.__brisa.append(ponto)
    
    def tell_limite_x(self, x):
        self.__limite[0] = x
    
    def tell_limite_y(self, y):
        self.__limite[1] = y

    def ask_fedor(self, ponto):
        return ponto in self.__fedor

    def ask_brisa(self, ponto):
        return ponto in self.__brisa

    def ask_wumpus(self, ponto):
        if not wp.dentro_limite(ponto, self.__limite):
            return False

        if (ponto in self.ask_visitados()):
            return False

        wumpus = True
        for a in wp.calcular_adjacentes_limitados(ponto, self.__limite):
            if (not self.ask_fedor(a)):
                wumpus = False

        return wumpus

    def ask_poco(self, ponto):
        if not wp.dentro_limite(ponto, self.__limite):
            return False

        if (ponto in self.ask_visitados()):
            return False

        poco = True
        for a in wp.calcular_adjacentes_limitados(ponto, self.__limite):
            if not self.ask_brisa(a):
                poco = False

        return poco

    def ask_visitados(self):
        return self.__visitados

    def ask_nao_seguro(self, ponto):
        visitados = self.ask_visitados()
        if (ponto in visitados):
            return False

        seguro_fedor = False
        seguro_brisa = False
        for a in wp.calcular_adjacentes_limitados(ponto, self.__limite):
            if a in visitados:
                if (not self.ask_fedor(a)):
                    seguro_fedor = True

                if (not self.ask_brisa(a)):
                    seguro_brisa = True

        return not (seguro_fedor and seguro_brisa)

    def ask_seguro(self, ponto):
        return not self.ask_nao_seguro(ponto)
    
    def tell_wumpus_morto(self):
        self.__fedor = []