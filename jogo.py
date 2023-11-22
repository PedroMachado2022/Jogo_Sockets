import pygame

import random

# Inicialize o Pygame
pygame.init()

# Defina as dimensões da janela
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
unidade_mapa = 33.4

# Variaveis de jogo
jogadores = [
            {'id': 1, 'cor': 'verde'},
            {'id': 2, 'cor': 'vermelho'},
            {'id': 3, 'cor': 'amarelo'},
            {'id': 4, 'cor': 'azul'}
            ]

player1 = pygame.image.load("imgs/player1j.png")
player2 = pygame.image.load("imgs/player2j.PNG")
player3 = pygame.image.load("imgs/player3j.PNG")
player4 = pygame.image.load("imgs/player4j.PNG")

dado_image = pygame.image.load("imgs/player4.PNG")


font = pygame.font.Font('./font/04b.ttf', 28)
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
    def __init__(self, jogador, posicao, posicao_inicial, imagem):
        self.jogador = jogador
        self.posicao_base = posicao
        self.posicao = posicao
        self.preso = True 
        self.contador_geral = 0
        self.posicao_inicial = posicao_inicial
        self.imagem = imagem
    
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
                nova_peca = Peca(self.players[i], peca_player[i][z], pos_incial[i], player1)
                self.pecas.append(nova_peca)

    
    def Desenhar(self):
        for i in self.pecas:
            i.Desenhar_peca()
    
    def atualizar_pecas(self, lista, turno):
   
        for i, z in enumerate(lista):
            self.pecas[i].Att(z)
        
        if self.turno != turno:
            print('chega aqui no turno jogo')
            
            self.turno = turno
        

    def Dado(self):
        show_image = None
        self.dado = 6 #random.randint(, 6)
            
    def Imagem_Dado(self):
        show_image = None
        if self.dado == 1:
            show_image = dado_image
        elif self.dado == 2:
            pass
        elif self.dado == 3:
            pass
        elif self.dado == 4:
            pass
        elif self.dado == 5:
            pass
        else:
            pass

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
dado_size = 50
dado_rect = pygame.Rect(SCREEN_WIDTH - dado_size - 20, SCREEN_HEIGHT // 2 - dado_size // 2, dado_size, dado_size)



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

# # Loop principal
# while True:
#     for evento in pygame.event.get():
#         if evento.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit()
        
#         # ---------------------Evento de click no dado---------------
#         if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:  # Botão esquerdo do mouse
#             mouse_click_position = pygame.mouse.get_pos()

#             # Se o clique do mouse estiver dentro da área do quadrado do dado
#             if dado_rect.collidepoint(mouse_click_position):
#                 if mouse_click_position:
#                     dado_pos = mouse_click_position
#                 if jogo.dado == 0 and jogo.jogou == False:
#                     jogo.Dado()
#                     jogo.Imagem_Dado()
#                     for i in jogo.pecas:
#                         if i.jogador == jogo.players[jogo.turno]:
#                             if i.preso == False or jogo.dado == 6:
#                                 jogo.jogou = True
#                     print('Debug: dado', jogo.dado)
#                     if jogo.jogou == False:
#                         jogo.proximo_turno()


        #----------------------Evento de click nas pecas----------- 
        # if jogo.jogou == True: #verificar se o player jogou o dado
        #     if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:  
        #             mouse_x, mouse_y = pygame.mouse.get_pos()
        
        #             # Verifica se o clique ocorreu em uma peça
        #             for peca in jogo.pecas:
        #                 peca_x = (unidade_mapa * peca.posicao[0]) + x
        #                 peca_y = (unidade_mapa * peca.posicao[1]) + y

        #                 # Se o clique do mouse estiver dentro da área da peça
        #                 if peca_x - 15 <= mouse_x <= peca_x + 15 and peca_y - 15 <= mouse_y <= peca_y + 15:

        #                     if jogo.players[jogo.turno] == peca.jogador: #Vez do player
        #                         if peca.preso == True and jogo.dado == 6: #liberar peça
        #                             peca.posicao = peca.posicao_inicial
        #                             peca.preso = False
        #                             #sistema de troca de turno
        #                             jogo.proximo_turno()

        #                         elif peca.preso == False:
        #                             peca.Andar(jogo.dado, jogo.pecas)
        #                             #sistema de troca de turno
        #                             jogo.proximo_turno()


    # # Desenha na tela
    # screen.fill(DARK_GRAY)
    # screen.blit(mapa, (50, 50))

    # # Desenha a imagem resposta do dado quando a posição do click for diferente de (0,0)
    # if dado_pos != (0, 0):
    #     screen.blit(dado_image, dado_pos)
    

    # if jogo.ganhou != -1:
    #     screen.blit(font.render('Player '+str(jogo.ganhou['id'])+' VENCEU!', True, branco), (180, 15))
    # else:
    #     screen.blit(font.render('Player '+str(jogo.turno+1), True, branco), (220, 15))
    # #dado
    # pygame.draw.rect(screen, branco, dado_rect)
    # pygame.draw.rect(screen, preto, dado_rect, 2) 
    
   

    # # Desenha as peças
    # jogo.Desenhar()
    # # Atualiza a tela
    # pygame.display.flip()
