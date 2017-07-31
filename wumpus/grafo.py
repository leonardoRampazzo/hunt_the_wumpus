import wumpus.ponto as wp

class GrafoMapa:
    def __init__(self, limite):
        self.limite = limite
        self.pontos_visitados = set([])
    
    def visitados(self, ponto):
        return ponto in self.pontos_visitados
    
    def adjacentes(self, ponto):
        adjacentes = wp.calcular_adjacentes_limitados(ponto, self.limite)
        adjacentes = filter(self.visitados, adjacentes)
        return adjacentes
        
class GrafoMapaCusto(GrafoMapa):
    def __init__(self, limite):
        super().__init__(limite)
        self.custos = {}
    
    def custo(self, from_node, to_node):
        return self.custos.get(to_node, 1)