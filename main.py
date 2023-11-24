'''

'''

import pygame
import sys
import servidor.scTCP as tcp
import threading
from time import sleep
from jogo import *


pygame.init()


#variaveis server
Conexao_Tcp = tcp.ClienteTCP(0)
HOST = "127.0.0.1"
PORT = 65432

#variavel de Input --> (Buscar partida)
user_text = ''

# Cores
preto = (0,0,0)
DARK_GRAY = (30, 30, 50)
branco = (255, 255, 255)
vermelho = (255, 0, 0)
verde = (100, 200, 100)
azul = (0, 0, 255)
amarelo = (255, 255, 0)


# Cor do texto
cor_texto = branco

# Tamanho da janela
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Fonte
font = pygame.font.Font('./font/04b.ttf', 28)
font2 = pygame.font.Font('./font/04b.TTF', 16)

# Criar a janela
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Carregar a imagem de fundo
background = pygame.image.load("imgs/BACKGROUND.PNG")

# Criar Botão
create_button = font.render("Criar uma Partida", True, DARK_GRAY)
find_button = font.render("Encontrar uma Partida", True, DARK_GRAY)

# Escolher posiçao dos botoes
create_rect = create_button.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
find_rect = find_button.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))

# Quadrado central 

center_square = pygame.Surface((600, 400), pygame.SRCALPHA)
center_square.fill(DARK_GRAY)

#texto do numero da sala

Number_room = font.render("Codigo sala:", True, preto)
Number_room_r = Number_room.get_rect(center=(SCREEN_WIDTH // 2, 120))

#texto de volta
exit = font.render("Sair", True, preto)
exit_r = exit.get_rect(center=((SCREEN_WIDTH // 2)-220, 120))

#texto de start
Start = font.render("Start", True, preto)
Start_r = Start.get_rect(center=((SCREEN_WIDTH // 2), 400))

# pecas grafica

player1 = pygame.image.load("imgs/player1.png")
player2 = pygame.image.load("imgs/player2.PNG")
player3 = pygame.image.load("imgs/player3.PNG")
player4 = pygame.image.load("imgs/player4.PNG")

# Tiulo do jogo
pygame.display.set_caption("Ludo")

#inicar servidor

Conexao_Tcp.conectar(HOST, PORT)

# Thread com objetivo de ficar escutando mensagens do servidor
threading.Thread(target=Conexao_Tcp.receber_mensagens).start()


jogo_objeto = None

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN :

            #Criar Partida
            if create_rect.collidepoint(event.pos) and Conexao_Tcp.page == 0:
                Conexao_Tcp.page = 1
                Conexao_Tcp.enviar_mensagem("Create_room/")
                print('Sala Criada')
                sleep(0.1)
                Conexao_Tcp.atualizar()
                
            #sair a pagina
            elif exit_r.collidepoint(event.pos) and (Conexao_Tcp.page == 1 or Conexao_Tcp.page == 3):
                if Conexao_Tcp.page == 1:
                    Conexao_Tcp.sair()
                Conexao_Tcp.page = 0
                Conexao_Tcp.page=0
                print('sair')

            #Começar Jogo
            elif Start_r.collidepoint(event.pos) and Conexao_Tcp.page == 1:
                Conexao_Tcp.Iniciar_jogo()
                jogo_objeto = Jogo()
                jogo_objeto.iniciar(Conexao_Tcp.players)            
                Conexao_Tcp.page = 4
               

            
            elif find_rect.collidepoint(event.pos) and Conexao_Tcp.page == 0:
                Conexao_Tcp.page = 3
                
    
            #Encontrar Partida
            elif Start_r.collidepoint(event.pos) and Conexao_Tcp.page == 3:
                #Buscar sala e limpar variavel
                Conexao_Tcp.Encontrar_sala(str(user_text))
                user_text = ''
                if Conexao_Tcp.sala != None:
                    Conexao_Tcp.page = 0
                else:
                    Conexao_Tcp.page = 1

            #verificar rodada

            #Jogo rodando                                 
            elif Conexao_Tcp.page == 4 and event.button == 1 and Conexao_Tcp.vez_de_jogar == True:

                mouse_click_position = pygame.mouse.get_pos()

                # Se o clique do mouse estiver dentro da área do quadrado do dado
                if dado_rect.collidepoint(mouse_click_position):
                    
                    if mouse_click_position:
                        dado_pos = mouse_click_position

                    if jogo_objeto.dado == 0 and jogo_objeto.jogou == False:
                        jogo_objeto.Dado()
                        jogo_objeto.Imagem_Dado()
                        imagem_dado = jogo_objeto.Imagem_Dado()
                        
                        
                        for i in jogo_objeto.pecas:
                            if i.jogador == jogo_objeto.players[jogo_objeto.turno]:
                                if i.preso == False or jogo_objeto.dado == 6:
                                    jogo_objeto.jogou = True

                        print('Debug: dado', jogo_objeto.dado)
                        if jogo_objeto.jogou == False:
                            jogo_objeto.proximo_turno()
                            print(jogo_objeto.turno)
                            Conexao_Tcp.vez_de_jogar= False
                            Conexao_Tcp.proximo_turno('Nada')


                #----------------------Evento de click nas pecas----------- 
                if jogo_objeto.jogou == True: #verificar se o player jogou o dado
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  
                            mouse_x, mouse_y = pygame.mouse.get_pos()
                
                            # Verifica se o clique ocorreu em uma peça
                            cont = 0
                            for peca in jogo_objeto.pecas:
                                cont +=1
                                peca_x = (unidade_mapa * peca.posicao[0]) + x
                                peca_y = (unidade_mapa * peca.posicao[1]) + y

                                # Se o clique do mouse estiver dentro da área da peça
                                if peca_x - 15 <= mouse_x <= peca_x + 15 and peca_y - 15 <= mouse_y <= peca_y + 15:

                                    if jogo_objeto.players[jogo_objeto.turno] == peca.jogador: #Vez do player
                                        cont -= 1
                                        if peca.preso == True and jogo_objeto.dado == 6: #liberar peça
                                            Conexao_Tcp.proximo_turno('Sair', cont)
                                            peca.posicao = peca.posicao_inicial
                                            peca.preso = False
                                            #sistema de troca de turno
                                            jogo_objeto.proximo_turno()
                                            Conexao_Tcp.vez_de_jogar= False


                                        elif peca.preso == False:
                                            Conexao_Tcp.proximo_turno('Andar', cont, jogo_objeto.dado)
                                            peca.Andar(jogo_objeto.dado, jogo_objeto.pecas)
                                            #sistema de troca de turno
                                            jogo_objeto.proximo_turno()
                                            Conexao_Tcp.vez_de_jogar= False


        #Escrever em pagina de busca
        elif event.type == pygame.KEYDOWN and Conexao_Tcp.page == 3:
            if event.key == pygame.K_RETURN:
                print(user_text)  
                user_text = ""    
            elif event.key == pygame.K_BACKSPACE:
                user_text = user_text[:-1]  
            elif event.unicode.isnumeric():  
                user_text += event.unicode
        
        # Funções de jogo
    
        
    # Pagina principal do jogo
    if Conexao_Tcp.page == 0:
        screen.blit(background, (0, 0))
        screen.blit(create_button, create_rect)
        screen.blit(find_button, find_rect)

    # Pagina de criaçao de partida
    elif Conexao_Tcp.page == 1:
        screen.blit(background, (0, 0))
        screen.blit(center_square, (100, 100))
        screen.blit(Number_room, Number_room_r)
        screen.blit(font.render(str(Conexao_Tcp.sala), True, preto), ((350, 140)))
        screen.blit(exit, exit_r)
        screen.blit(Start, Start_r)

        const = 220
        for i in range(1, (int(Conexao_Tcp.players)+1)):
            screen.blit(pygame.image.load("imgs/player"+str(i)+".png"), (const, 250))
            const += 100

    # Pagina para achar partida
    elif Conexao_Tcp.page == 3:

        screen.blit(background, (0, 0))
        screen.blit(center_square, (100, 100))
        screen.blit(font.render("Encontre", True, preto), (SCREEN_WIDTH // 2-100, 110))

        if not user_text:
            screen.blit(font.render('Digite um Numero!', True, preto), (220, 280))

        screen.blit(font.render(user_text, True, preto), (390-(len(user_text)*13), 280))

        screen.blit(exit, exit_r)
        screen.blit(font.render("Find", True, preto), Start_r)
    
    # Pagina quando começa o jogo
    elif Conexao_Tcp.page == 4:

        # Se não é o player que iniciou, inicia objeto do jogo.
        if jogo_objeto == None:
            jogo_objeto = Jogo()
            jogo_objeto.iniciar(Conexao_Tcp.players)

        screen.fill(DARK_GRAY)
        screen.blit(mapa, (50, 50))
        jogo_objeto.Atualiza_turno(Conexao_Tcp.turno)

        # Atulizar jogo com informações do turno de outros players
        if Conexao_Tcp.sair_base != -1:
            jogo_objeto.sair_peca(Conexao_Tcp.sair_base )
            Conexao_Tcp.sair_base = -1

        if Conexao_Tcp.andar:
            jogo_objeto.pecas[Conexao_Tcp.andar[0]].Andar(Conexao_Tcp.andar[1], jogo_objeto.pecas)
            jogo_objeto.verificapeca()
            Conexao_Tcp.andar = []
        #---------------------------------------------------------
        
        # Desenha a imagem resposta do dado quando a posição do click for diferente de (0,0)
        if jogo_objeto.dado != 0:
            screen.blit(imagem_dado, (SCREEN_WIDTH - dado_size - 100, SCREEN_HEIGHT // 2 - dado_size))
       
        # Mostrar na tela o player ganhador
        if jogo_objeto.ganhou != -1:
            screen.blit(font.render('Player '+str(jogo_objeto.ganhou['id'])+' VENCEU!', True, branco), (180, 15))
        else:
            jogador_atual = jogo_objeto.players[jogo_objeto.turno]
            jogador_cor = jogador_atual['cor']
            cor_texto = branco  

        # Ajuste das cores conforme a cor do jogador
        if jogador_cor == 'verde':
            cor_texto = verde
        elif jogador_cor == 'vermelho':
            cor_texto = vermelho
        elif jogador_cor == 'amarelo':
            cor_texto = amarelo
        elif jogador_cor == 'azul':
            cor_texto = azul
        screen.blit(font.render('Player '+str(jogo_objeto.turno+1), True, cor_texto), (220, 15))
    
        #pygame.draw.rect(screen, preto, dado_rect, 2) 
        screen.blit(font2.render(f'JOGAR', True, cor_texto), (SCREEN_WIDTH - dado_size - 60, SCREEN_HEIGHT // 2 - dado_size // 2))
     
        # Desenha as peças
        jogo_objeto.Desenhar()
        # Atualiza a tela
    
    pygame.display.flip()

pygame.quit()
sys.exit()
