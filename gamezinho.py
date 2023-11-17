# matriz = [
#     [1, 1, 1, 1, 1, 1, 7, 7, 3, 1, 1, 1, 1, 1, 1],
#     [1, 1, 1, 1, 1, 1, 5, 0, 3, 1, 1, 1, 1, 1, 1]
#     [1, 1, 1, 1, 1, 1, 5, 0, 3, 1, 1, 1, 1, 1, 1]
#     [1, 1, 1, 1, 1, 1, 5, 0, 3, 1, 1, 1, 1, 1, 1]
#     [1, 1, 1, 1, 1, 1, 5, 0, 3, 1, 1, 1, 1, 1, 1]
#     [1, 1, 1, 1, 1, 1, 5, 0, 9, 1, 1, 1, 1, 1, 1]
#     [7, 7, 7, 7, 7, 8, 'x', 'x', 'x', 7, 7, 7, 7, 7, 3]
#     [5, 0, 0, 0, 0, 0, 'x', 'x', 'x', 0, 0, 0, 0, 0, 3]
#     [5, 0, 0, 0, 0, 0, 'x', 'x', 'x', 2, 0, 0, 0, 0, 3]
#     [1, 1, 1, 1, 1, 1, 6, 0, 3, 1, 1, 1, 1, 1, 1]
#     [1, 1, 1, 1, 1, 1, 5, 0, 3, 1, 1, 1, 1, 1, 1]
#     [1, 1, 1, 1, 1, 1, 5, 0, 3, 1, 1, 1, 1, 1, 1]
#     [1, 1, 1, 1, 1, 1, 5, 0, 3, 1, 1, 1, 1, 1, 1]
#     [1, 1, 1, 1, 1, 1, 5, 0, 3, 1, 1, 1, 1, 1, 1]
#     [1, 1, 1, 1, 1, 1, 5, 0, 0, 1, 1, 1, 1, 1, 1]]
'''
#1 - ignora

#0 - 1 + esquerda
#3 - 1 + baixo
#5 - 1 + cima
#7 - 1 + direita

#2 - 1 + esqueda  + baixo
#6 - 1 + cima  + esquerda
#8 - 1 + direita + cima
#9 - 1 + baixo + direita

posiciona
#10 - azul
#11 - amarelo
#12 - verde
#13 - vermelho
'''

import pygame
import sys

# Inicialização do Pygame
pygame.init()

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Tamanho da tela e número de slots
SCREEN_SIZE = (600, 600)
ROWS, COLS = 15, 15
SLOT_SIZE = SCREEN_SIZE[0] // COLS

# Criar uma matriz 15x15
matrix = [[1]*COLS for _ in range(ROWS)]

# Definir 0 nas três linhas do meio
for i in range(ROWS//2 - 1, ROWS//2 + 2):
    matrix[i] = [0]*COLS

# Definir 0 nas três colunas do meio
for row in matrix:
    row[COLS//2 - 1:COLS//2 + 2] = [0]*3

# Inicialização da tela
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Matriz 15x15")

# Loop principal
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Desenhar a matriz na tela
    for i in range(ROWS):
        for j in range(COLS):
            color = WHITE if matrix[i][j] == 1 else BLACK
            pygame.draw.rect(screen, color, (j * SLOT_SIZE, i * SLOT_SIZE, SLOT_SIZE, SLOT_SIZE))

    # Atualizar a tela
    pygame.display.flip()