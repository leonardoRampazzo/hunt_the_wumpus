from unittest import TestCase, main

from wumpus.planejador import Planejador
from wumpus.posicao import Posicao, Direcao
from wumpus.base_dados_python import BaseDadosAgentePython
from wumpus.percepcao_agente import PercepcaoAgente
from wumpus.acao_agente import AcaoAgente


class TestPlanejador(TestCase):
    def adicionar_brisas(self, brisas):                
        for ponto in brisas:
            self.base_dados.tell_brisa(ponto)

    def adicionar_fedores(self, fedores):
        for ponto in fedores:
            self.base_dados.tell_fedor(ponto)

    def adicionar_visitados(self, visitados):
        for ponto in visitados:
            self.base_dados.tell_visitado(ponto)
            self.planejador.pontos_visitados.add(ponto)

    def setUp(self):
        self.base_dados = BaseDadosAgentePython()
        self.planejador = Planejador(
            base_dados=self.base_dados,
            limite=(4, 4),
            pontos_visitados=set([(1, 1)])
        )

    def tearDown(self):
        del self.planejador

    def teste_plano_simples(self):
        posicao_atual = Posicao((1, 1), Direcao.LESTE)
        plano = self.planejador.plano(posicao_atual.ponto())
        acao_plano = self.planejador.planejar(
            posicao_atual,
            {
                PercepcaoAgente.FEDOR: False,
                PercepcaoAgente.BRISA: False,
                PercepcaoAgente.BRILHO: False,
                PercepcaoAgente.WUMPUS_VIVO: True,
                PercepcaoAgente.VIVO: True,
                PercepcaoAgente.OURO_PEGO: False,
                PercepcaoAgente.DENTRO_CAVERNA: True
            }
        )

        self.assertEquals(plano, set([(1, 2), (2, 1)]),)
        self.assertEquals(acao_plano, AcaoAgente.ANDAR)

    def teste_plano_simples_2(self):    
        visitados = [
            (1,1), (2,1), (3,1)
        ]

        brisas = [
            (3, 1)
        ]

        pontos_seguros = [
            (1, 2), (2, 2),
        ]

        pontos_nao_seguros = [
            (3, 2), (4, 2)
        ]        
        posicao_atual = Posicao((3, 1), Direcao.LESTE)

        self.adicionar_brisas(brisas)
        self.adicionar_visitados(visitados)
        
        plano = self.planejador.plano(posicao_atual.ponto())
        acao_plano = self.planejador.planejar(
            posicao_atual,
            {
                PercepcaoAgente.FEDOR: True,
                PercepcaoAgente.BRISA: False,
                PercepcaoAgente.BRILHO: False,
                PercepcaoAgente.WUMPUS_VIVO: True,
                PercepcaoAgente.VIVO: True,
                PercepcaoAgente.OURO_PEGO: False,
                PercepcaoAgente.DENTRO_CAVERNA: True
            }
        )        
        self.assertSetEqual(plano, set([(1, 2), (2, 2)]),)
        self.assertEquals(acao_plano, AcaoAgente.RODAR_ESQUERDA)        


    def test_plano_medio(self):
        posicao_atual = Posicao((2, 4), Direcao.LESTE)        
        pontos_visitados = [
            (1, 4), (2, 4),         
            (1, 3), (2, 3), (3, 3), 
            (1, 2), (2, 2), (3, 2), (4, 2),
            (1, 1), (2, 1), (3, 1),
        ]                    

        brisas = [
            (2,4), (3,3)
        ]

        fedores = [
            (3,1),  (4,2)
        ]
        
        self.adicionar_brisas(brisas)
        self.adicionar_fedores(fedores)
        self.adicionar_visitados(pontos_visitados)
        
        plano = self.planejador.plano(posicao_atual.ponto())
        acao_plano = self.planejador.planejar(
            posicao_atual,
            {
                PercepcaoAgente.FEDOR: False,
                PercepcaoAgente.BRISA: True,
                PercepcaoAgente.BRILHO: False,
                PercepcaoAgente.WUMPUS_VIVO: True,
                PercepcaoAgente.VIVO: True,
                PercepcaoAgente.OURO_PEGO: False,
                PercepcaoAgente.DENTRO_CAVERNA: True
            }
        )        

        print(plano)
        
        self.assertSetEqual(plano, set([(4,3)]),)
        self.assertEquals(acao_plano, AcaoAgente.RODAR_DIREITA)
        

if __name__ == '__main__':
    main()
