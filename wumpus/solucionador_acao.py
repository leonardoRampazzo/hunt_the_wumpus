import math
from wumpus.acao_agente import AcaoAgente
from wumpus.direcao import Direcao
import wumpus.ponto as wp

import logging

module_logger = logging.getLogger('wumpus_application.logger')

class SolucionadorAcao:
    def __init__(self, pontos_visitado=set([]), base_dados = None):
        self.pontos_visitados = pontos_visitado        
        self.base_dados = base_dados
        self.logger = logging.getLogger(
            'wumpus_application.solucionador_acao.SolucionadorAcao')
        self.logger.info('Criando uma instancia de SolucionadorAcao')

    def __ponto_mais_perto__(self, plano, ponto_atual):
        ponto_mais_perto = None
        distancia_ponto_mais_perto = math.inf
        for ponto in plano:
            if ponto != ponto_atual:                
                distancia = wp.calcular_distancia(ponto_atual, ponto)
                if distancia_ponto_mais_perto > distancia:            
                    ponto_mais_perto = ponto
                    distancia_ponto_mais_perto = distancia   
        return ponto_mais_perto              
    
    def __melhor_acao_atirar__(self, plano, posicao_atual):
        ponto_andar = posicao_atual.calcular_posicao(AcaoAgente.ANDAR).ponto()
        return self.base_dados.ask_wumpus(ponto_andar)

    def __melhor_acao_andar__(self, plano, posicao_atual):        
        ponto_atual = posicao_atual.ponto()
        ponto_andar = posicao_atual.calcular_posicao(AcaoAgente.ANDAR).ponto()
                
        if ponto_andar in plano:
            return True               

        if ponto_andar in self.pontos_visitados:
            for ponto_plano in plano:            
                if ponto_plano in posicao_atual.adjacentes():                    
                    return False

            for ponto_plano in plano:                                     
                if (wp.calcular_distancia(ponto_andar, ponto_plano)
                        < wp.calcular_distancia(ponto_atual, ponto_plano)):
                    return True                        

        return False

    def __melhor_acao_virar_esquerda__(self, plano, posicao_atual):        
        ponto_atual = posicao_atual.ponto()        
        direcao_atual = posicao_atual.direcao()
                                
        ponto_mais_perto = self.__ponto_mais_perto__(plano, ponto_atual)
        if ponto_mais_perto:
            self.logger.info('Ponto atual: {}'.format(ponto_atual))
            self.logger.info('Ponto mais perto: {}'.format(ponto_mais_perto))

            ref_x, ref_y =  wp.subtrair_pontos(ponto_mais_perto, ponto_atual)
            
            ref_direcao_x = None
            ref_direcao_y = None

            self.logger.info('Ref X: {}'.format(ref_x))
            self.logger.info('Ref Y: {}'.format(ref_y))
            
            if ref_x > 0:
                ref_direcao_x = Direcao.LESTE
            elif ref_x < 0:
                ref_direcao_x = Direcao.OESTE

            if ref_y > 0:
                ref_direcao_y = Direcao.NORTE
            elif ref_y < 0:
                ref_direcao_y = Direcao.SUL

            self.logger.info('Ref Direcao X: {}'.format(ref_direcao_x))
            self.logger.info('Ref Direcao Y: {}'.format(ref_direcao_y))

            if (direcao_atual == Direcao.NORTE
                    and ref_direcao_x == Direcao.OESTE):
                    return True
            elif (direcao_atual == Direcao.SUL
                    and ref_direcao_x == Direcao.LESTE):
                    return True
            elif (direcao_atual == Direcao.LESTE
                    and ref_direcao_y == Direcao.NORTE):
                    return True
            elif (direcao_atual == Direcao.OESTE
                    and ref_direcao_y == Direcao.SUL):
                    return True
        
        return False
        
    
    def solucionar(self, plano, posicao_atual):
        if self.__melhor_acao_atirar__(plano, posicao_atual):
            self.logger.info('Matou wumpus')
            return AcaoAgente.MATAR_WUMPUS
        
        if self.__melhor_acao_andar__(plano, posicao_atual):            
            self.logger.info('Andou')
            return AcaoAgente.ANDAR

        if self.__melhor_acao_virar_esquerda__(plano, posicao_atual):
            self.logger.info('Virou esquerda')
            return AcaoAgente.RODAR_ESQUERDA

        self.logger.info('Virou direita')
        return AcaoAgente.RODAR_DIREITA
