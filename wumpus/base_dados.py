import abc


class BaseDadosAgente(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def tell_visitado(self, ponto):
        pass

    def tell_fedor(self, ponto):
        pass

    @abc.abstractmethod
    def tell_brisa(self, ponto):
        pass

    @abc.abstractmethod
    def tell_ouro(self, ponto):
        pass

    @abc.abstractmethod
    def ask_fedor(self, ponto):
        pass

    @abc.abstractmethod
    def ask_brisa(self, ponto):
        pass

    @abc.abstractmethod
    def ask_ouro(self, ponto):
        pass

    @abc.abstractmethod
    def ask_wumpus(self, ponto):
        pass

    @abc.abstractmethod
    def ask_poco(self, ponto):
        pass
        
    @abc.abstractmethod
    def ask_visitados(self):
        pass

    @abc.abstractmethod
    def tell_limite_x(self, x):
        pass

    @abc.abstractmethod
    def tell_limite_y(self, y):
        pass

    @abc.abstractmethod
    def tell_wumpus_morto(self):
        pass