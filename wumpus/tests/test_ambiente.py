import unittest
from wumpus.ambiente_wumpus import AmbienteWumpus, PontoInvalidoGeracaoAmbiente
from wumpus.percepcao_ambiente import PercepcaoAmbiente


class TestAmbiente(unittest.TestCase):
    def setUp(self):
        self.ambiente = AmbienteWumpus((4, 4))

    def tearDown(self):
        del self.ambiente

    def teste_geracao_ambiente_vazio(self):
        self.assertTrue(self.ambiente.ouro((4, 4)))
        for x in range(1, 5):
            for y in range(1, 5):
                ponto = (x, y)
                self.assertFalse(self.ambiente.wumpus(ponto))
                self.assertFalse(self.ambiente.poco(ponto))

    def teste_geracao_ambiente_um_wumpus_dois_pocos(self):
        self.ambiente.add_poco((2, 1))
        self.ambiente.add_poco((2, 2))
        self.ambiente.add_wumpus((3, 2))

        self.assertTrue(self.ambiente.ouro((4, 4)))
        self.assertTrue(self.ambiente.wumpus((3, 2)))
        self.assertTrue(self.ambiente.poco((2, 1)))
        self.assertTrue(self.ambiente.poco((2, 2)))

    def teste_excecao_ponto_invalido(self):
        with self.assertRaises(PontoInvalidoGeracaoAmbiente):
            self.ambiente.add_poco((1, 1))
            self.ambiente.add_wumpus((1, 1))
            self.ambiente.add_ouro((1, 1))

    def teste_percepcao(self):
        """
        x x X x
        x x x x
        P O W x 
        x x x x
        """
        self.ambiente.add_poco((1, 2))
        self.ambiente.add_wumpus((3, 2))
        self.ambiente.add_ouro((2, 2))

        p = self.ambiente.percepcao((2, 2))

        self.assertTrue(p[PercepcaoAmbiente.BRILHO])
        self.assertTrue(p[PercepcaoAmbiente.FEDOR])
        self.assertTrue(p[PercepcaoAmbiente.BRISA])

        p = self.ambiente.percepcao((4, 2))
        self.assertFalse(p[PercepcaoAmbiente.BRILHO])
        self.assertTrue(p[PercepcaoAmbiente.FEDOR])
        self.assertFalse(p[PercepcaoAmbiente.BRISA])


if __name__ == '__main__':
    unittest.main()
