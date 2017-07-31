from wumpus.agente_wumpus import AgenteWumpus
from wumpus.ambiente_wumpus import AmbienteWumpus
from wumpus.base_dados_python import BaseDadosAgentePython
from wumpus.posicao import Posicao, Direcao
from wumpus.wumpus_log import WumpusLog
from pprint import pprint


def main():
    log = WumpusLog()

    ambiente = AmbienteWumpus((4, 4))
    ambiente.add_wumpus((4, 1))
    ambiente.add_poco((3, 4))
    base_agente = BaseDadosAgentePython()

    i = 0
    agente = AgenteWumpus(ambiente, base_agente)
    while (agente.executando()):
        i += 1    
#    for i in range(1, 34):
        print("Executando ação Nº {} do agente:".format(i))
        print("------------------------")
        print("Posição atual: {}".format(agente.posicao()))
        print("Retorno execução: {}".format(agente.executar_acao_automatica()))
        print("Retorno execução: {}".format(agente.executando()))        
        print("Percepção: {}".format(agente.percepcao()))
        print("------------------------")


if __name__ == '__main__':
    main()
