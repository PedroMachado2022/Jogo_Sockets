'''
Script com toda a logica do jogo 
'''

import pygame
import sys
import random
pygame.init()

# Defina as dimensões da janela
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
unidade_mapa = 33.4

jogadores = [{'id': 1, 'cor': 'verde'},
             {'id': 2, 'cor': 'vermelho'},
             {'id': 3, 'cor': 'amarelo'},
             {'id': 4, 'cor': 'azul'}]

# Variaveis de jogo
player1 = pygame.image.load("imgs/player1j.png")
player2 = pygame.image.load("imgs/player2j.PNG")
player3 = pygame.image.load("imgs/player3j.PNG")
player4 = pygame.image.load("imgs/player4j.PNG")

dado_1 = pygame.image.load("imgs/dado_1.png")
dado_2 = pygame.image.load("imgs/dado_2.png")
dado_3 = pygame.image.load("imgs/dado_3.png")
dado_4 = pygame.image.load("imgs/dado_4.png")
dado_5 = pygame.image.load("imgs/dado_5.png")
dado_6 = pygame.image.load("imgs/dado_6.png")

start_button = pygame.image.load("imgs/start.png")


font  = pygame.font.Font('./font/04b.ttf', 28)
font2  = pygame.font.Font('./font/04b.ttf', 28)


x = 67
y = 67
matriz_jogo = [
    [1, 1, 1, 1, 1, 1, 7, 7, 3, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 5, 3, 3, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 5, 3, 3, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 5, 3, 3, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 5, 3, 3, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 5, 3, 9, 1, 1, 1, 1, 1, 1],
    [7, 7, 7, 7, 7, 8, 1, 4, 1, 7, 7, 7, 7, 7, 3],
    [5, 7, 7, 7, 7, 7, 4, 1, 4, 0, 0, 0, 0, 0, 3],
    [5, 0, 0, 0, 0, 0, 1, 4, 1, 2, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 6, 5, 3, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 5, 5, 3, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 5, 5, 3, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 5, 5, 3, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 5, 5, 3, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 5, 0, 0, 1, 1, 1, 1, 1, 1]]

peca_player = [[[1.5, 2.5],[2.5, 1.5],[3.5, 2.5],[2.5, 3.5]], 
               [[10.5, 2.5],[11.5, 1.5],[12.5, 2.5],[11.5, 3.5]], 
               [[1.5, 11.5],[2.5, 10.5],[3.5, 11.5],[2.5, 12.5]], 
               [[10.5, 11.5],[11.5, 10.5],[12.5, 11.5],[11.5, 12.5]]]


pos_incial = [[1, 6], [8, 1], [6, 13], [13,8]]

def regra(pos, cont):
    num = matriz_jogo[pos[1]][pos[0]]
    #1 - ignora
    
    #0 - 1 + esquerda || andou 51 blocos + 1 cima
    if num == 0:
        if cont == 51:
            pos = [pos[0],pos[1]-1] 
        else:    
            pos = [pos[0]-1,pos[1]] 
    #3 - 1 + baixo || andou 51 blocos + 1 esquerda
    elif num == 3:
        if cont == 51:
            pos = [pos[0]-1,pos[1]] 
        else:
            pos = [pos[0],pos[1]+1] 
    #5 - 1 + cima || andou 51 blocos + 1 direita
    elif num == 5:
        if cont == 51:
            pos = [pos[0]+1,pos[1]] 
        else:
            pos = [pos[0],pos[1]-1] 
    #7 - 1 + direita || andou 51 blocos + 1 baixo
    elif num == 7:
        if cont == 51:
            pos = [pos[0],pos[1]+1]
        else:
            pos = [pos[0]+1,pos[1]] 
    #2 - 1 + esqueda  + baixo
    elif num == 2:
        pos = [pos[0]-1,pos[1]+1] 
    #6 - 1 + cima  + esquerda
    elif num == 6:
        pos = [pos[0]-1,pos[1]-1] 
    #8 - 1 + direita + cima
    elif num == 8:
        pos = [pos[0]+1,pos[1]-1] 
    #9 - 1 + baixo + direita
    elif num == 9:
        pos = [pos[0]+1,pos[1]+1] 
    elif num == 4:
        pos = 'ganhou'
    
    return pos

# Controle de peças
class Peca:
    def __init__(self, jogador, posicao, posicao_inicial):
        self.jogador = jogador
        self.posicao_base = posicao
        self.posicao = posicao
        self.preso = True 
        self.contador_geral = 0
        self.posicao_inicial = posicao_inicial
        
        
    def Desenhar_peca(self):
    # Desenha as peças de cada jogador
        jogador_cor = self.jogador['cor']
        jogador_imagem = None

        if jogador_cor == 'verde':
            jogador_imagem = player3
        elif jogador_cor == 'vermelho':
            jogador_imagem = player2
        elif jogador_cor == 'amarelo':
            jogador_imagem = player4
        elif jogador_cor == 'azul':
            jogador_imagem = player1

        # Desenhar a imagem do jogador na tela
        if jogador_imagem:
            jogador_rect = jogador_imagem.get_rect()
            jogador_rect.center = ((unidade_mapa * self.posicao[0]) + x, (unidade_mapa * self.posicao[1]) + y)
            screen.blit(jogador_imagem, jogador_rect)

    def morre(self):
        print('debug: morreu ', self.posicao)
        self.posicao = self.posicao_base
        self.preso = True

    def Att(self, nova_pos):
        if self.posicao[0] != nova_pos[0] or self.posicao[1] != nova_pos[1]:
            
            self.posicao = nova_pos
            print('mudou')


        
    def Andar(self, dado, pecas):
        
            if self.preso == False:
                
                # ---- Verificar contador**
                for i in range(dado):
                    self.contador_geral += 1
                    self.posicao = regra(self.posicao, self.contador_geral)
                    if self.posicao == 'ganhou':
                        pecas.remove(self)
                        break

                for i in pecas:
                    if i.jogador != self.jogador:

                        if i.posicao == self.posicao:
                            i.morre()

# Controle de jogo
class Jogo:
    def __init__(self):

        self.players = None
        
        self.pecas = []
        self.turno = 0
        self.dado = 0
        self.jogou = False
        self.ganhou = -1

    def iniciar(self, num):
        self.players = jogadores[0:num]
        for i in range(num):
            for z in range(0, 4):
                nova_peca = Peca(self.players[i], peca_player[i][z], pos_incial[i])
                self.pecas.append(nova_peca)

    
    def Desenhar(self):
        for i in self.pecas:
            i.Desenhar_peca()
    
    def sair_peca(self, peca):
        self.pecas[peca].posicao = self.pecas[peca].posicao_inicial
        self.pecas[peca].preso = False

    def Atualiza_turno(self,turno):
        
        if self.turno != turno:
            print('chega aqui no turno jogo')
            
            self.turno = turno
        

    def Dado(self):
        self.dado = random.randint(1, 6)
            
    def Imagem_Dado(self):
        if self.dado == 1:
            show_image = dado_1
        elif self.dado == 2:
            show_image = dado_2
        elif self.dado == 3:
            show_image = dado_3
        elif self.dado == 4:
            show_image = dado_4
        elif self.dado == 5:
            show_image = dado_5
        elif self.dado == 6:
            show_image = dado_6
        else:
            show_image = None
        return show_image
    def verificapeca(self):
        
        for i in self.players:
            ganhou = 0
            for z in self.pecas:
                if i == z.jogador:
                    ganhou = 1
            if ganhou == 0:
                self.ganhou = i

        print(self.ganhou)

    def proximo_turno(self):
        self.verificapeca()
        self.jogou = False
        self.dado = 0
        if self.turno == (len(self.players)-1):
            self.turno = 0
        else: 
            self.turno+= 1
        print("Debug: Next_Turno", self.turno)   

        

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Ludo')

# mapa
mapa = pygame.image.load("imgs/mapa.PNG")

#dado
dado_size = 20
dado_rect = pygame.Rect(SCREEN_WIDTH - dado_size - 60, SCREEN_HEIGHT // 1.7 - dado_size // 2, dado_size + 100, dado_size)



# Defina as cores
preto = (0,0,0)
DARK_GRAY = (30, 30, 50)
branco = (255, 255, 255)
vermelho = (255, 0, 0)
verde = (100, 200, 100)
azul = (0, 0, 255)
amarelo = (255, 255, 0)

mouse_click_position = None

dado_pos = (0,0)

haha = False

