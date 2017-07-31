from wumpus.direcao import Direcao
import math


def dentro_limite(ponto, limite):
    x, y = ponto
    return 0 < x <= limite[0] and 0 < y <= limite[1]


def somar_pontos(p1, p2):
    return tuple(x + y for x, y in zip(p1, p2))


def subtrair_pontos(p1, p2):
    return tuple(x - y for x, y in zip(p1, p2))


def calcular_adjacentes(ponto):
    return [
        somar_pontos(ponto, Direcao.NORTE.value),
        somar_pontos(ponto, Direcao.SUL.value),
        somar_pontos(ponto, Direcao.LESTE.value),
        somar_pontos(ponto, Direcao.OESTE.value)
    ]


def limitar_pontos(pontos, limite):
    pontos = filter(lambda ponto: dentro_limite(ponto, limite), pontos)
    return pontos


def calcular_adjacentes_limitados(ponto, limite):
    return limitar_pontos(calcular_adjacentes(ponto), limite)


def calcular_distancia(a, b):
    xa, ya = a
    xb, yb = b

    return math.sqrt(math.pow((xa - xb), 2) + math.pow((ya - yb), 2))
