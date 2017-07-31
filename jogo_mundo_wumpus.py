import tkinter as tki
import tkinter.ttk as ttk
from tkinter import  Label, Button, LEFT, TOP, X, FLAT, RAISED, SUNKEN, PhotoImage, Frame, Text, END, INSERT
from PIL import Image, ImageTk

from wumpus.agente_wumpus import AgenteWumpus
from wumpus.percepcao_agente import PercepcaoAgente
from wumpus.ambiente_wumpus import AmbienteWumpus
from wumpus.base_dados_python import BaseDadosAgentePython
from wumpus.posicao import Posicao, Direcao
from wumpus.wumpus_log import WumpusLog
from pprint import pprint

import time

log = WumpusLog()

class Cave:
    def __init__(self):
        self.root = tki.Tk()
        self.root.title("Mundo de Wumpus")
        self.root.geometry("800x550+0+0")
        self.velocidade_jogo = 500
        self.preco_coro_wumpus = 500
        self.add_posicoes()
        self.add_mapa()
        self.pontos = 1000
        self.root.mainloop()                
        
        
    def start(self):
        self.preco_coro_wumpus = 500
        self.pontos = 1000
        self.remove_on_log()
        self.add_mapa()
        self.loop()

    def loop(self):
        posicao, acao = self.agente.executar_acao_automatica()        
        self.i += 1       
        
        (x, y)   = posicao.ponto()
        direcao  = posicao.direcao()
        self.move_agente((x, y,direcao))
        self.muda_pontuacao()        
        self.logtext += ("-------------------------------\n")
        self.logtext += ("Executando ação Nº {} do agente \n".format(self.i))
        self.logtext += ("Ação do agente: {} \n".format(acao))
        self.logtext += ("Posição do agente: ({}, {}) \n".format(x,y))
        self.logtext += ("Direção do agente: {} \n".format(direcao))                
        p = self.agente.percepcao()
        if(not p[PercepcaoAgente.WUMPUS_VIVO]):
            self.monstro_morreu()

        if(self.agente.executando()):
            self.add_on_log()
            self.logtext = ""
            self.root.after(self.velocidade_jogo,self.loop)
        else:
            if p[PercepcaoAgente.OURO_PEGO]:
                self.logtext += ("-------------------------------\n")
                self.logtext += ("Parabéns! Você recuperou o ouro e saiu da caverna! \n")                
                self.pontos += 1000                
            else:
                self.logtext += ("-------------------------------\n")
                self.logtext += ("Você morreu!\n")
                self.pontos = 0
                                    
            self.pontos += 10                                    
            self.muda_pontuacao()                                                                        
            self.logtext += ('Pontuação final: {} \n'.format(self.pontos))
            self.logtext += ("-------------------------------\n")            
            self.add_on_log()        

    def add_on_log(self):
        self.text.insert(END,self.logtext)
        self.text.see("end")

    def remove_on_log(self):
        self.logtext = ""
        self.i = 0
        self.text.delete('1.0', END)

    def muda_velocidade(self,event):
        if self.selectVel.get() == "Devagar":
            self.velocidade_jogo = 1250
        elif self.selectVel.get() == "Normal":
            self.velocidade_jogo = 1000
        elif self.selectVel.get() == "Rápido":
            self.velocidade_jogo = 500
        else:
            self.velocidade_jogo = 100

    def add_posicoes(self):
        self.add_botoes_a_grid()
        self.buttonGO = Button(text="Start :>",command=self.start)
        self.buttonGO.grid(row=5,column=4)

        self.select = ttk.Combobox(width=10,value=['Facil', 'Médio', 'Dificil' , 'impossivel'])
        self.select.set("Facil")
        self.select.bind("<<ComboboxSelected>>", self.execute)
        self.select.state(['readonly'])
        self.select.grid(row=5,column=2)
        

        self.selectVel = ttk.Combobox(width=10,value=['Devagar', 'Normal', 'Rápido' , 'Flash'])
        self.selectVel.set("Devagar")
        self.selectVel.bind("<<ComboboxSelected>>", self.muda_velocidade)
        self.selectVel.state(['readonly'])
        self.selectVel.grid(row=6,column=2)

        self.label = Label(text="Pontos: 1000")
        self.label.grid(row=5,column=7)

        self.label1 = Label(text="Dificuldade:")
        self.label1.grid(row=5,column=1)

        self.label2 = Label(text="Velocidade:")
        self.label2.grid(row=6,column=1)

        self.text        = Text(height=30,width=50)
        self.text.grid(row=1,column=5,columnspan=3,rowspan=4,padx=5,pady=5)


    def muda_pontuacao(self):
        self.pontos -= 10
        self.label["text"] = "Pontos: {}".format(self.pontos)

    def execute(self,event):
        self.remove_on_log()
        self.add_mapa()

    def add_mapa(self):
        self.add_botoes_a_grid()
        self.ambiente = AmbienteWumpus((4, 4))
        
        if self.select.get() == "Facil":
            gold    = (4, 4)
            monstro = (4, 1)
            pocos   =  [(1,4)]

        if(self.select.get() == "Médio"):
            gold    = (4, 4)
            monstro = (4, 3)
            pocos   =  [ (1,4), (4,1) ]

        if(self.select.get() == "Dificil"):
            gold    = (4, 4)
            monstro = (4, 1)
            pocos   =  [(3, 4), (1, 4), (1, 3) ]

        if(self.select.get() == "impossivel"):
            gold    = (3, 3)
            monstro = (3, 1)
            pocos   =  [
                (1,3),
                (4,2),
                (4,4),                
            ]

        
        self.posiciona_monstro(monstro)
        self.ambiente.add_wumpus(monstro)
        self.posiciona_gold(gold)
        self.ambiente.add_ouro(gold)

        for poco in pocos:
            self.posiciona_poco(poco)
            self.ambiente.add_poco(poco)

        self.base_agente = BaseDadosAgentePython()
        self.agente = AgenteWumpus(self.ambiente, self.base_agente)
        self.posiciona_agente((1,1,"Direcao.LESTE"))
        

    def add_botoes_a_grid(self):
        self.btun = {}
        y = 4
        for i in range(1,5):
            for j in range(1,5):
                self.btun[j, i] = Button(padx=50,pady=50)
                self.btun[j, i].grid(row=y,column=j)
            y = y - 1

    def addImage(self, nome):
        imagem = Image.open(nome)
        imagem1 = imagem.resize((100, 115))
        imagem1 = ImageTk.PhotoImage(imagem1)
        return imagem1

    def posiciona_monstro(self,posicao):
        self.posicao_monstro = posicao
        x,y=posicao 
        image = self.addImage("imagens/monstrinho.jpg")
        self.btun[x, y].config(image= image)
        self.btun[x, y].image = image

    def monstro_morreu(self):
        if self.preco_coro_wumpus > 0:
            self.pontos += self.preco_coro_wumpus
            self.logtext += ("Loot do wumpus: Couro, {} pontos \n".format(self.preco_coro_wumpus))
        self.preco_coro_wumpus = 0
        x,y=self.posicao_monstro
        image = self.addImage("imagens/monstro_morreu.jpg")
        self.btun[x, y].config(image= image)
        self.btun[x, y].image = image

    def posiciona_gold(self,posicao):
        self.posicao_gold = posicao
        x,y=posicao 
        image = self.addImage("imagens/Ouro.jpg")
        self.btun[x, y].config(image= image)
        self.btun[x, y].image = image

    def pego_gold(self):
        x,y=self.posicao_gold
        image = self.addImage("imagens/Ouro_pego.jpg")
        self.btun[x, y].config(image= image)
        self.btun[x, y].image = image

    def posiciona_poco(self,posicao):
        x,y=posicao 
        image = self.addImage("imagens/poco.jpg")
        self.btun[x, y].config(image= image)
        self.btun[x, y].image = image

    def posiciona_agente(self,posicao):
        self.posicao_agente = posicao
        x,y,z=posicao 
        nome = "imagens/agente_{}.gif".format(z)
        image = self.addImage(nome)
        self.btun[x, y].config(image= image)
        self.btun[x, y].image = image

    def move_agente(self,posicao):
        posicao_ant = self.posicao_agente 
        x,y,z=posicao_ant
        row,col = self.conversao_para_grid((x, y))

        if(not self.posicao_monstro == (x, y)):
            self.btun[x, y] = Button(padx=47,pady=49,text="v")
            self.btun[x, y].grid(row=row,column=col)

        self.posiciona_agente(posicao)


    def rotaciona_agente(self,posicao):
        posicao_ant = self.posicao_agente 
        x,y,z,row,col=posicao_ant
        self.posiciona_agente(posicao)

    def conversao_para_grid(self,ponto):
        x,y = ponto

        if(y == 1):
             xn = 4
        elif(y == 2):
             xn = 3
        elif(y == 3):
             xn = 2
        else:
             xn = 1
        yn = x

        return (xn , yn)

if __name__ == "__main__":
    cave = Cave()