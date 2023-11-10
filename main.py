import pygame
import sys

pygame.init()


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

center_square = pygame.Surface((600, 350), pygame.SRCALPHA)
center_square.fill(BLACK_transparent)


pygame.display.set_caption("Ludo")

page = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if create_rect.collidepoint(event.pos) & page == 0:
                # Lógica para criar uma partida
                page = 1
                print("Criar uma partida")
            elif find_rect.collidepoint(event.pos):
                # Lógica para encontrar uma partida
                print("Encontrar uma partida")

    if page == 0:
        # Desenhar a imagem de fundo
        screen.blit(background, (0, 0))


        # Desenhar botoes
        screen.blit(create_button, create_rect)
        screen.blit(find_button, find_rect)

    if page == 1:

        screen.blit(background, (0,0))
        screen.blit(center_square, (100,100))
    pygame.display.flip()

pygame.quit()
sys.exit()
