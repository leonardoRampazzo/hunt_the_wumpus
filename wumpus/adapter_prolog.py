from pyswip import Query, Prolog, Functor, Variable, call
from pyswip import Prolog


class AdapterProlog:
    def __init__(self):
        self.__prolog = Prolog()

    def __is_false__(self, query):
        return len(list(query)) == 0

    def query_fato(self, fato):
        return not self.__is_false__(self.__prolog.query(fato))

    def query_funcao(self, funcao):
        return self.__prolog.query(funcao)

    def consult(self, path):
        self.__prolog.consult(path)

    def assertz(self, assertion):
        self.__prolog.assertz(assertion)
