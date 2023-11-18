import pygame
import sys
import random

# Inicialize o Pygame
pygame.init()

# Defina as dimensões da janela
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
unidade_mapa = 33.4

# Variaveis de jogo
x = 67
y = 67
matriz_jogo = [
    [1, 1, 1, 1, 1, 1, 7, 7, 3, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 5, 3, 3, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 5, 3, 3, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 5, 3, 3, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 5, 3, 3, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 5, 3, 9, 1, 1, 1, 1, 1, 1],
    [7, 7, 7, 7, 7, 8, 1, 1, 1, 7, 7, 7, 7, 7, 3],
    [5, 7, 7, 7, 7, 7, 1, 1, 1, 0, 0, 0, 0, 0, 3],
    [5, 0, 0, 0, 0, 0, 1, 1, 1, 2, 0, 0, 0, 0, 0],
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
    print('debug: ', pos)
    return pos

# Controle de peças
class Peca:
    def __init__(self, jogador, posicao, posicao_inicial):
        self.jogador = jogador
        self.posicao = posicao
        self.preso = True 
        self.contador_geral = 0
        self.posicao_inicial = posicao_inicial
    
    def Desenhar_peca(self):
        #print()
        pygame.draw.circle(screen, self.jogador['cor'], ((unidade_mapa * self.posicao[0]) + x,  (unidade_mapa * self.posicao[1]) + y), 15)
    
    def Andar(self, dado):
        
        print('debug: peça andou ', dado)
        if self.preso == False:
            
            # ---- Verificar contador**
            for i in range(dado):
                self.contador_geral += 1
                self.posicao = regra(self.posicao, self.contador_geral)


# Controle de jogo
class Jogo:
    def __init__(self):

        self.players = [
            {'id': 1, 'cor': (100, 200, 100)}, 
            {'id': 2, 'cor': (255, 200, 200)}, 
            {'id': 3, 'cor': (200, 200, 100)}, 
            {'id': 4, 'cor': (200, 100, 255)}]
        
        self.pecas = []
        self.turno = 0
        self.dado = 0
        self.jogou = False

    def iniciar(self):
        for i in range(len(self.players)):
            for z in range(0,4):
                nova_peca = Peca(self.players[i], peca_player[i][z], pos_incial[i])
                self.pecas.append(nova_peca)
    

    def Desenhar(self):
        for i in self.pecas:
            i.Desenhar_peca()
    
    def Dado(self):
        self.dado = random.randint(5, 6)

    def proximo_turno(self):
        print("Debug: Next_Turno", self.turno)
        self.jogou = False
        self.dado = 0
        if self.turno == (len(self.players)-1):
            self.turno = 0
        else: 
            self.turno+= 1

        



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

jogo = Jogo()

jogo.iniciar()

# Loop principal
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:  # Botão esquerdo do mouse
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Se o clique do mouse estiver dentro da área do quadrado do dado
            if dado_rect.collidepoint(mouse_x, mouse_y):
                if jogo.dado == 0 and jogo.jogou == False:
                    jogo.Dado()
                    for i in jogo.pecas:
                        if i.jogador == jogo.players[jogo.turno]:
                            if i.preso == False or jogo.dado == 6:
                                jogo.jogou = True
                    print('Debug: dado', jogo.dado)           
                    if jogo.jogou == False:
                        jogo.proximo_turno()


        #----------------------Evento de click nas pecas----------- 
        if jogo.jogou == True: #verificar se o player jogou o dado
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:  
                    mouse_x, mouse_y = pygame.mouse.get_pos()
        
                    # Verifica se o clique ocorreu em uma peça
                    for peca in jogo.pecas:
                        peca_x = (unidade_mapa * peca.posicao[0]) + x
                        peca_y = (unidade_mapa * peca.posicao[1]) + y

                        # Se o clique do mouse estiver dentro da área da peça
                        if peca_x - 15 <= mouse_x <= peca_x + 15 and peca_y - 15 <= mouse_y <= peca_y + 15:

                            if jogo.players[jogo.turno] == peca.jogador: #Vez do player
                                if peca.preso == True and jogo.dado == 6: #liberar peça
                                    peca.posicao = peca.posicao_inicial
                                    peca.preso = False
                                    #sistema de troca de turno
                                    jogo.proximo_turno()
                                elif peca.preso == False:
                                    peca.Andar(jogo.dado)
                                    #sistema de troca de turno
                                    jogo.proximo_turno()


    # Desenha na tela
    screen.fill(DARK_GRAY)
    screen.blit(mapa, (50, 50))

    #dado
    pygame.draw.rect(screen, branco, dado_rect)
    pygame.draw.rect(screen, preto, dado_rect, 2) 

    # Desenha as peças
    jogo.Desenhar()
    # Atualiza a tela
    pygame.display.flip()
