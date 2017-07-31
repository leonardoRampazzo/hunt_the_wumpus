from wumpus.acao_agente import AcaoAgente
from wumpus.posicao import Posicao, Direcao
from wumpus.base_dados import BaseDadosAgente
from wumpus.ambiente_wumpus import PercepcaoAmbiente
from wumpus.planejador import Planejador
from wumpus.percepcao_agente import PercepcaoAgente

import logging

# create logger
module_logger = logging.getLogger('wumpus_application.agente')


class AgenteWumpus:
    def __init__(self, ambiente, base_agente):
        self.logger = logging.getLogger(
            'wumpus_application.agente.AgenteWumpus')
        self.__posicao_atual = Posicao((1, 1), Direcao.LESTE)
        self.__ambiente = ambiente
        self.__base_dados = base_agente

        self.__pontos_visitados = set([])

        self.__vivo = True
        self.__ouro_pego = False
        self.__dentro_caverna = True
        self.__numero_flechas = 1
        self.__wumpus_morto = False

    def executar_acao_automatica(self):
        self.logger.info('Executando executar_acao')
        self.logger.info("Posicao Atual: {}".format(str(self.__posicao_atual)))

        self.__tell_visitado__()
        self.__tell_percepcao_atual__()

        acao_planejada = self.__planejar__()
        self.executar_acao(acao_planejada)

        self.logger.info("Nova posição: {}".format(self.__posicao_atual))
        self.logger.info("Acao planejada: {}".format(str(acao_planejada)))

        return (self.__posicao_atual, acao_planejada)

    def executar_acao(self, acao, tell_base=True):
        if tell_base:
            self.__tell_visitado__()
            self.__tell_percepcao_atual__()

        if acao == AcaoAgente.MATAR_WUMPUS:
            self.__executar_acao_atirar_flecha__()
        elif acao == AcaoAgente.PEGAR_OURO:
            self.__executar_acao_pegar_ouro__()
        else:
            self.__executar_acao_movimentacao__(acao)

    def percepcao(self):
        ponto_atual = self.__posicao_atual.ponto()
        pa = self.__ambiente.percepcao(ponto_atual)

        return {
            PercepcaoAgente.FEDOR: pa[PercepcaoAmbiente.FEDOR],
            PercepcaoAgente.BRISA: pa[PercepcaoAmbiente.BRISA],
            PercepcaoAgente.BRILHO: pa[PercepcaoAmbiente.BRILHO],
            PercepcaoAgente.WUMPUS_VIVO: not pa[PercepcaoAmbiente.GRITO],
            PercepcaoAgente.VIVO: self.__vivo,
            PercepcaoAgente.OURO_PEGO: self.__ouro_pego,
            PercepcaoAgente.DENTRO_CAVERNA: self.__dentro_caverna
        }

    def posicao(self):
        return self.__posicao_atual

    def executando(self):
        p = self.percepcao()
        return (p[PercepcaoAgente.VIVO]
                and p[PercepcaoAgente.DENTRO_CAVERNA])

    def __tell_visitado__(self):
        ponto = self.__posicao_atual.ponto()
        self.__base_dados.tell_visitado(ponto)
        self.__pontos_visitados.add(ponto)

    def __tell_percepcao_atual__(self):
        ponto_atual = self.__posicao_atual.ponto()
        percepcao_atual = self.__ambiente.percepcao(ponto_atual)

        if percepcao_atual[PercepcaoAmbiente.BRISA]:
            self.__base_dados.tell_brisa(ponto_atual)

        if percepcao_atual[PercepcaoAmbiente.FEDOR]:
            self.__base_dados.tell_fedor(ponto_atual)

    def __planejar__(self):
        self.logger.info('Executando __planejar__')
        planejador = Planejador(
            base_dados=self.__base_dados,
            limite=self.__ambiente.limite(),
            pontos_visitados=self.__pontos_visitados,
        )
        percepcao = self.percepcao()
        plano = planejador.planejar(self.__posicao_atual, percepcao)
        self.logger.info("Percepcao: {}".format(percepcao))
        self.logger.info("Plano {}".format(plano))
        return plano

    def __executar_acao_atirar_flecha__(self):
        if self.__numero_flechas > 0:
            self.__numero_flechas -= 1
            self.__ambiente.atirar_flecha(self.__posicao_atual)
            wumpus_gritou = self.__ambiente.percepcao(self.__posicao_atual.ponto())[
                PercepcaoAmbiente.GRITO]
            if wumpus_gritou:
                self.__wumpus_morto = True
                self.__base_dados.tell_wumpus_morto()

    def __executar_acao_pegar_ouro__(self):
        self.__ouro_pego = True
        self.__ambiente.pegar_ouro(self.__posicao_atual.ponto())

    def __executar_acao_movimentacao__(self, acao):
        self.__posicao_atual = self.__posicao_atual.calcular_posicao(acao)
        ponto_atual = self.__posicao_atual.ponto()

        if (self.__ambiente.wumpus(ponto_atual)
                or self.__ambiente.poco(ponto_atual)):
            self.__vivo = False

        p = self.percepcao()

        if (p[PercepcaoAgente.VIVO]
                and (p[PercepcaoAgente.OURO_PEGO]
                     and (ponto_atual == (1, 1)))):
            self.__dentro_caverna = False

    def pontos_visitados(self):
        return self.__pontos_visitados
