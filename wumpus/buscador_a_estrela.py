from wumpus.priority_queue import PriorityQueue
from wumpus.grafo import GrafoMapaCusto
import wumpus.ponto as wp

class BuscadorAEstrela:
    def __init__(self, grafo):
        self.grafo = grafo
        self.__custo_ate_ponto = {}
        self.__antecedente_ponto = {}    
        self.__origem = None
        self.__objetivo = None

    def heuristica(self, p1, p2):
        return wp.calcular_distancia(p1, p2)

    def __ponto_menor_custo__(self, ponto, custo):
        return (ponto not in self.__custo_ate_ponto
                    or custo < self.__custo_ate_ponto[ponto])

    def __calcular_custo__(self, ponto_atual, ponto):
        return (self.__custo_ate_ponto[ponto_atual]
                    + self.grafo.custo(ponto_atual, ponto))

    def buscar(self, origem, objetivo):
        self.__origem = origem
        self.__objetivo = objetivo

        pilha_priorizada = PriorityQueue()
        pilha_priorizada.put(origem, 0)

        self.__custo_ate_ponto = {}
        self.__antecedente_ponto = {}

        self.__antecedente_ponto[origem] = None
        self.__custo_ate_ponto[origem] = 0

        while not pilha_priorizada.empty():
            ponto_atual = pilha_priorizada.get()

            if ponto_atual == objetivo:
                break

            for ponto in self.grafo.adjacentes(ponto_atual):
                novo_custo = self.__calcular_custo__(ponto_atual, ponto)

                if self.__ponto_menor_custo__(ponto, novo_custo):
                    self.__antecedente_ponto[ponto] = ponto_atual
                    self.__custo_ate_ponto[ponto] = novo_custo                                    
                    pilha_priorizada.put(
                        ponto, 
                        novo_custo + self.heuristica(objetivo, ponto)
                    )                    

        return (self.__antecedente_ponto, self.__custo_ate_ponto)

    def melhor_caminho(self):
        caminho = set([])      

        if self.__objetivo:
            atual = self.__objetivo                  
            while atual is not None:                        
                caminho.add(atual)
                if atual in self.__antecedente_ponto:
                    atual = self.__antecedente_ponto[atual]
                else: atual = None
                
        return caminho
