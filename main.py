import pygame
import sys
import servidor.scTCP as tcp
import threading
import socket

pygame.init()

#variaveis server
Conexao_Tcp = tcp.ClienteTCP()
HOST = "127.0.0.1"
PORT = 65432



#variaveis game

players = [1,2]

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


# Controle de pagina
page = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if create_rect.collidepoint(event.pos) and page == 0:
                page = 1
                Conexao_Tcp.enviar_mensagem("Create_room")
                print('Sala Criada')
                # code = int(tcp.receive_message())
                # print("Criar uma sala, Código:", code)
            elif exit_r.collidepoint(event.pos) and page != 0:
                page = 0
                tcp.send_message("Leave_room")
                print('sair')
            elif Start_r.collidepoint(event.pos) and page == 1:
                page = 0
                print('Start')
            elif find_rect.collidepoint(event.pos) and page == 0:
                page = 3
                tcp.send_message("Find_room")
                response = tcp.receive_message()
                print("Resposta do servidor:", response)
            elif Start_r.collidepoint(event.pos) and page == 3:
                page = 3
                print("Encontrar uma partida")

    if page == 0:
        # Desenhar a imagem de fundo
        screen.blit(background, (0, 0))


        # Desenhar botoes
        screen.blit(create_button, create_rect)
        screen.blit(find_button, find_rect)

    if page == 1:
        #tcp.Atualizar(tcp.sock)
        screen.blit(background, (0,0))
        screen.blit(center_square, (100,100))
        screen.blit(Number_room, Number_room_r)
        screen.blit(exit,exit_r)
        screen.blit(Start,Start_r)
        
        const = 220
        for i in players:
            screen.blit(pygame.image.load("imgs/player"+str(i)+".png"), (const, 250))
            const+=100

    if page == 3:
        screen.blit(background, (0,0))
        screen.blit(center_square, (100,100))
        screen.blit(font.render("Encontre", True, BLACK), (SCREEN_WIDTH // 2-100, 110))
        screen.blit(exit,exit_r)
        screen.blit(font.render("Find", True, BLACK),Start_r)


    pygame.display.flip()

pygame.quit()
sys.exit()
