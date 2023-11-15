import pygame
import sys
import servidor.scTCP as tcp
import threading
from time import sleep
pygame.init()

#variaveis server
Conexao_Tcp = tcp.ClienteTCP()
HOST = "127.0.0.1"
PORT = 65432

#variavel de Input

user_text = ''

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLACK_transparent = (50, 50, 150, 200)
DARK_GRAY = (30, 30, 50)


# Tamanho da janela
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Fonte
font = pygame.font.Font('./font/04b.ttf', 28)

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
center_square.fill(BLACK_transparent)

#texto do numero da sala

Number_room = font.render("Codigo sala:", True, BLACK)
Number_room_r = Number_room.get_rect(center=(SCREEN_WIDTH // 2, 120))

#texto de volta
exit = font.render("Sair", True, BLACK)
exit_r = exit.get_rect(center=((SCREEN_WIDTH // 2)-220, 120))

#texto de start
Start = font.render("Start", True, BLACK)
Start_r = Start.get_rect(center=((SCREEN_WIDTH // 2), 400))

# pecas grafica

player1 = pygame.image.load("imgs/player1.png")
player2 = pygame.image.load("imgs/player2.PNG")
player3 = pygame.image.load("imgs/player1.PNG")
player4 = pygame.image.load("imgs/player2.PNG")

# Tiulo do jogo
pygame.display.set_caption("Ludo")

#inicar servidor

Conexao_Tcp.conectar(HOST, PORT)

# iniciar escuta de servidor 

threading.Thread(target=Conexao_Tcp.receber_mensagens).start()

# Controle de pagina
page = 0


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:

            #Criar Partida
            if create_rect.collidepoint(event.pos) and page == 0:
                page = 1
                Conexao_Tcp.enviar_mensagem("Create_room ")
                print('Sala Criada')
                sleep(0.1)
                Conexao_Tcp.atualizar()
                
            #sair a pagina
            elif exit_r.collidepoint(event.pos) and page != 0:
                if page == 1:
                    Conexao_Tcp.sair()
                page = 0
                print('sair')

            #Começar Jogo
            elif Start_r.collidepoint(event.pos) and page == 1:
                page = 0
                print('Start')

            
            elif find_rect.collidepoint(event.pos) and page == 0:
                page = 3
                
    
            #Encontrar Partida
            elif Start_r.collidepoint(event.pos) and page == 3:
                #Buscar sala e limpar variavel
                Conexao_Tcp.Encontrar_sala(str(user_text))
                user_text = ''
                if Conexao_Tcp.sala != None:
                    page = 0
                else:
                    page = 1                    
                
        #Escrever em pagina de busca
        elif event.type == pygame.KEYDOWN and page == 3:
            if event.key == pygame.K_RETURN:
                print(user_text)  
                user_text = ""    
            elif event.key == pygame.K_BACKSPACE:
                user_text = user_text[:-1]  
            elif event.unicode.isnumeric():  
                user_text += event.unicode


    if page == 0:
        # Desenhar a imagem de fundo
        screen.blit(background, (0, 0))

        # Desenhar botões
        screen.blit(create_button, create_rect)
        screen.blit(find_button, find_rect)

    elif page == 1:
        screen.blit(background, (0, 0))
        screen.blit(center_square, (100, 100))
        screen.blit(Number_room, Number_room_r)
        screen.blit(font.render(str(Conexao_Tcp.sala), True, BLACK), ((350, 140)))
        screen.blit(exit, exit_r)
        screen.blit(Start, Start_r)

        const = 220
        for i in range(1, (int(Conexao_Tcp.players)+1)):
            screen.blit(pygame.image.load("imgs/player"+str(i)+".png"), (const, 250))
            const += 100

    elif page == 3:
        screen.blit(background, (0, 0))
        screen.blit(center_square, (100, 100))
        screen.blit(font.render("Encontre", True, BLACK), (SCREEN_WIDTH // 2-100, 110))

        if not user_text:
            screen.blit(font.render('Digite um Numero!', True, BLACK), (220, 280))

        screen.blit(font.render(user_text, True, BLACK), (390-(len(user_text)*13), 280))

        screen.blit(exit, exit_r)
        screen.blit(font.render("Find", True, BLACK), Start_r)



    pygame.display.flip()

pygame.quit()
sys.exit()
