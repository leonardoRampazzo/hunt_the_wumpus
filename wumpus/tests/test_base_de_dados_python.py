import unittest
from wumpus.base_dados_python import BaseDadosAgentePython


class TestBaseDeDadosPython(unittest.TestCase):
    def setUp(self):
        self.base = BaseDadosAgentePython()

    def tearDown(self):
        del self.base

    def teste_wumpus(self):
        self.base.tell_fedor((2, 1))
        self.base.tell_fedor((1, 2))
        self.base.tell_fedor((2, 3))
        self.base.tell_fedor((3, 2))

        self.assertTrue(self.base.ask_wumpus((2, 2)))

    def teste_poco(self):
        self.base.tell_brisa((2, 1))
        self.base.tell_brisa((1, 2))
        self.base.tell_brisa((2, 3))
        self.base.tell_brisa((3, 2))

        self.assertTrue(self.base.ask_poco((2, 2)))

    def teste_seguro(self):
        visitados = [
            (1, 1), (2, 1), (3, 1)
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

        for ponto in visitados:
            self.base.tell_visitado(ponto)

        for ponto in brisas:
            self.base.tell_brisa(ponto)

        self.assertSetEqual(
            self.base.ask_visitados(),
            set(visitados)
        )

        self.assertTrue(self.base.ask_brisa((3, 1)))

        for ponto in pontos_seguros:
            self.assertTrue(self.base.ask_seguro(ponto))

        for ponto in pontos_nao_seguros:
            self.assertFalse(self.base.ask_seguro(ponto))

    def teste_seguro_hard(self):
        fedores = [
            (4, 2), (3, 1)
        ]
        brisas = [
            (2, 4), (3, 3), (4, 4)
        ]
        pontos_visitados = [
            (2, 4),         (4, 4),
            (1, 3), (2, 3), (3, 3), (4, 3),
            (1, 2), (2, 2),         (4, 2),
            (1, 1), (2, 1), (3, 1),
        ]

        for fedor in fedores:
            self.base.tell_fedor(fedor)

        for brisa in brisas:
            self.base.tell_brisa(brisa)

        for ponto in pontos_visitados:
            self.base.tell_visitado(ponto)

        self.assertTrue(self.base.ask_seguro((3, 2)))
        self.assertTrue(self.base.ask_seguro((1, 4)))

    def teste_seguro_hardest(self):
        fedores = [
            (4, 2), (3, 1)
        ]
        brisas = [
            (2, 4), (3, 3)
        ]
        pontos_visitados = [
            (1, 4), (2, 4),
            (1, 3), (2, 3), (3, 3),
            (1, 2), (2, 2), (3, 2), (4, 2),
            (1, 1), (2, 1), (3, 1),
        ]

        for fedor in fedores:
            self.base.tell_fedor(fedor)

        for brisa in brisas:
            self.base.tell_brisa(brisa)

        for ponto in pontos_visitados:
            self.base.tell_visitado(ponto)

        self.assertTrue(self.base.ask_seguro((4, 3)))
        self.assertFalse(self.base.ask_seguro((3, 4)))
        self.assertFalse(self.base.ask_seguro((4, 1)))


if __name__ == '__main__':
    unittest.main()
