import pygame
import sys
import random

# Inicialize o Pygame
pygame.init()

# Defina as dimensões da janela
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
unidade_mapa = 33

# Grid jogável bloco de 33
x = (unidade_mapa * 2) + 167
y = (unidade_mapa * 6) + 69

peca_player = [[(2.5, 2.5),(3.5, 1.5),(4.5, 2.5),(3.5, 4.5)]]

class Peca:
    def __init__(self, jogador, posicao):
        self.jogador = jogador
        self.posicao = posicao

class Jogo:
    def __init__(self):
        self.players = ['p1']
        self.pecas = []
        self.dado = 0
    
    def iniciar(self):
        for i in self.players:
            for z in range(0,4):
                nova_peca = Peca(i, peca_player[i][z])
                self.pecas.append(nova_peca)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Ludo')

# mapa
mapa = pygame.image.load("imgs/mapa.PNG")

# Defina as cores
DARK_GRAY = (30, 30, 50)
branco = (255, 255, 255)
vermelho = (255, 0, 0)
verde = (0, 255, 0)
azul = (0, 0, 255)
amarelo = (255, 255, 0)

jogo = Jogo()

# Loop principal
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Atualizações do jogo

    # Simula o lançamento de dados
    if pygame.mouse.get_pressed()[0]:  # Botão esquerdo do mouse pressionado
        jogo.dado = random.randint(1, 6)
        print("Dado:", jogo.dado)

    # Desenha na tela
    screen.fill(DARK_GRAY)
    screen.blit(mapa, (150, 50))

    # Desenha as peças
    for peca in jogo.pecas:
        pygame.draw.circle(screen, vermelho, (x + peca.posicao * 20, y), 15)

    # Atualiza a tela
    pygame.display.flip()
