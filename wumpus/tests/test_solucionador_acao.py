import unittest

from wumpus.posicao import Posicao, Direcao
from wumpus.solucionador_acao import SolucionadorAcao
from wumpus.acao_agente import AcaoAgente
from wumpus.base_dados_python import BaseDadosAgentePython


class TestPosicao(unittest.TestCase):
    def setUp(self):
        self.base = BaseDadosAgentePython()
        self.solucionador = SolucionadorAcao(base_dados=self.base)

    def tearDown(self):
        del self.solucionador

    def test_solucao_andar_frente(self):
        posicao = Posicao((1, 1), Direcao.LESTE)
        plano_1 = set([(2, 1)])
        plano_2 = set([(2, 1), (1, 2)])

        self.assertEqual(
            self.solucionador.solucionar(plano_1, posicao),
            AcaoAgente.ANDAR
        )

        self.assertEqual(
            self.solucionador.solucionar(plano_2, posicao),
            AcaoAgente.ANDAR
        )

    def test_solucao_voltar_1_quadrado(self):
        self.solucionador.pontos_visitados = set([
            (1, 1),
            (2, 1),
            (3, 1)
        ])
        plano = set([(1, 2), (2, 2)])
        posicao_inicial = Posicao((3, 1), Direcao.LESTE)
        print(posicao_inicial)

        posicao = posicao_inicial
        for _ in range(1, 6):
            acao = self.solucionador.solucionar(plano, posicao)
            posicao = posicao.calcular_posicao(acao)

        self.assertEqual(
            posicao.ponto(),
            (2, 2)
        )

    def test_solucao_hard(self):
        posicao_inicial = Posicao((2, 4), Direcao.LESTE)
        self.solucionador.pontos_visitados = set([
            (1, 1), (2, 1), (3, 1),
            (2, 2), (2, 3), (2, 4),
        ])
        plano = set([(3, 3)])

        posicao = posicao_inicial
        for i in range(1, 7):
            acao = self.solucionador.solucionar(plano, posicao)
            posicao = posicao.calcular_posicao(acao)

        self.assertEqual(
            posicao.ponto(),
            (3, 3)
        )

    def test_solucao_voltar_ouro_pego(self):
        posicao_inicial = Posicao((4, 4), Direcao.SUL)
        self.solucionador.pontos_visitados = set([
            (1, 1), (1, 2), (1, 3),
            (2, 1), (2, 2), (2, 3), (2, 4),
            (3, 1), (3, 2), (3, 3),
            (4, 2), (4, 3), (4, 4),
        ])
        plano = set([(1, 1)])

        posicao = posicao_inicial
        for i in range(1, 20):
            acao = self.solucionador.solucionar(plano, posicao)
            posicao = posicao.calcular_posicao(acao)

        self.assertEqual(
            posicao.ponto(),
            (1, 1)
        )


if __name__ == '__main__':
    unittest.main()
