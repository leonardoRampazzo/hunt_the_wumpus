from wumpus.adapter_prolog import AdapterProlog
from wumpus.base_dados import BaseDadosAgente

import os
import abc


class BaseDadosProlog:
    def __init__(self):
        self._prolog = AdapterProlog()

    def load_from_file(self, caminho_arquivo):
        self._prolog.consult(caminho_arquivo)

    def _tell_(self, fato, valor):
        return self._prolog.assertz('{}{}'.format(fato, valor))

    def _ask_(self, fato, valor):
        return self._prolog.query_fato('{}{}'.format(fato, valor))

@BaseDadosAgente.register
class BaseDadosAgenteProlog(BaseDadosProlog):
    def __init__(self):
        BaseDadosProlog.__init__(self)
        self.load_from_file(
            os.path.join(os.getcwd(), "prolog", "agente.pl")
        )

    def tell_fedor(self, ponto):
        return self._tell_('fedor', str(ponto))

    def tell_brisa(self, ponto):
        return self._tell_('brisa', str(ponto))

    def tell_ouro(self, ponto):
        return self._tell_('ouro', str(ponto))

    def ask_fedor(self, ponto):
        return self._ask_('fedor', str(ponto))

    def ask_brisa(self, ponto):
        return self._ask_('brisa', str(ponto))

    def ask_ouro(self, ponto):
        return self._ask_('ouro', str(ponto))

    def ask_wumpus(self, ponto):
        pass

    def ask_poco(self, ponto):
        pass
    
    def kill_wumpus(self, ponto):
        pass
        