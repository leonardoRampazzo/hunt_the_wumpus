from wumpus.acao_agente import AcaoAgente
from wumpus.percepcao_agente import PercepcaoAgente
from wumpus.solucionador_acao import SolucionadorAcao
import wumpus.ponto as wp

import logging

# create logger
module_logger = logging.getLogger('wumpus_application.logger')


class Planejador:
    def __init__(self, base_dados, limite=(4, 4), pontos_visitados=set([])):
        self.logger = logging.getLogger(
            'wumpus_application.planejador.Planejador')
        self.logger.info('Criando uma instancia de Planejador')
        self.limite = limite
        self.pontos_visitados = pontos_visitados
        self.__base_dados = base_dados

    def planejar(self, posicao_atual, percepcao):
        self.logger.info("Planejando")

        if percepcao[PercepcaoAgente.OURO_PEGO]:
            self.logger.info("Planejando volta")
            plano = self.__planejar_volta__(posicao_atual.ponto())
        elif percepcao[PercepcaoAgente.BRILHO]:
            self.logger.info("Brilhando! pegar o ouro!")
            return AcaoAgente.PEGAR_OURO
        else:
            plano = self.plano(posicao_atual.ponto())

        self.logger.info("Planejamento {}: {}".format(len(plano), plano))
        self.logger.info("Visitados {}: {}".format(
            len(self.pontos_visitados),
            self.pontos_visitados
        ))

        solucionador = SolucionadorAcao(
            pontos_visitado=self.pontos_visitados,
            base_dados=self.__base_dados
        )
        return solucionador.solucionar(
            plano, posicao_atual
        )

    def plano(self, ponto_atual):
        plano = self.__planejar_atirar__(ponto_atual)
        if not plano:
            plano = self.__planejar_seguros__()
            if not plano:
                plano = self.__planejar_nao_seguro__()

        return plano

    def __planejar_volta__(self, ponto_atual):
        from wumpus.grafo import GrafoMapaCusto
        from wumpus.buscador_a_estrela import BuscadorAEstrela    
        
        grafo_mapa = GrafoMapaCusto((4, 4))
        grafo_mapa.pontos_visitados = self.pontos_visitados                
        destino = (1,1)
        
        buscador = BuscadorAEstrela(grafo_mapa)
        buscador.buscar(ponto_atual, destino)

        return buscador.melhor_caminho()

    def __planejar_atirar__(self, ponto_atual):
        self.logger.info("Planejando atirar")
        plano = set([])

        for ponto_adjacente in wp.calcular_adjacentes_limitados(ponto_atual, self.limite):
            if (ponto_adjacente not in self.pontos_visitados
                    and self.__base_dados.ask_wumpus(ponto_adjacente)):
                plano.add(ponto_adjacente)

        return plano

    def __planejar_seguros__(self):
        self.logger.info("Planejando seguros")
        return self.__adjacentes_seguros__()

    def __planejar_nao_seguro__(self):
        self.logger.info("Planejando não seguros")
        return self.__adjacentes__()

    def __adjacentes__(self):
        adjacentes_nao_visitados = set([])

        for ponto_visitado in self.pontos_visitados:
            for ponto_adjacente in wp.calcular_adjacentes_limitados(ponto_visitado, self.limite):
                if ponto_adjacente not in self.pontos_visitados:
                    adjacentes_nao_visitados.add(ponto_adjacente)

        return adjacentes_nao_visitados

    def __adjacentes_seguros__(self):
        adjacentes_seguros = set([])

        for ponto_visitado in self.pontos_visitados:
            self.logger.info(
                "Buscando pontos seguros do ponto {}".format(str(ponto_visitado)))
            for ponto_adjacente in wp.calcular_adjacentes_limitados(ponto_visitado, self.limite):
                if ponto_adjacente not in self.pontos_visitados:
                    if self.__base_dados.ask_seguro(ponto_adjacente):
                        self.logger.info(
                            "Ponto adjacente seguro {}".format(str(ponto_adjacente)))
                        adjacentes_seguros.add(ponto_adjacente)

        return adjacentes_seguros
