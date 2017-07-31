import unittest
from wumpus.posicao import *
from wumpus.acao_agente import AcaoAgente


class TestPosicao(unittest.TestCase):
    def setUp(self):
        self.posicao = Posicao((1, 1), Direcao.LESTE)

    def tearDown(self):
        del self.posicao

    def teste_rodacao_invalida(self):
        with self.assertRaises(RotacaoDirecaoInvalida):
            self.posicao.rodar(Direcao.OESTE)

    def teste_andar_duas_vezes_norte(self):
        self.posicao = self.posicao.rodar(Direcao.NORTE)
        self.posicao = self.posicao.andar()
        self.posicao = self.posicao.andar()
        self.assertEqual(self.posicao.ponto(), (1, 3))

    def teste_andar_duas_vezes_leste(self):
        self.posicao = self.posicao.andar()
        self.posicao = self.posicao.andar()
        self.assertEqual(self.posicao.ponto(), (3, 1))

    def teste_andar_duas_vezes_norte_acao(self):
        self.posicao = self.posicao.calcular_posicao(AcaoAgente.RODAR_ESQUERDA)
        self.posicao = self.posicao.calcular_posicao(AcaoAgente.ANDAR)
        self.posicao = self.posicao.calcular_posicao(AcaoAgente.ANDAR)

    def testar_acao_que_nao_movimenta(self):
        self.posicao = self.posicao.calcular_posicao(AcaoAgente.PEGAR_OURO)


if __name__ == '__main__':
    unittest.main()
