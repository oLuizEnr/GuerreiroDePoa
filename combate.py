import pygame
import os

# Inicializa o Pygame
pygame.init()

# Define os diretórios de forma padrão (idependente da maquina)
dirPrincipal = os.path.dirname(__file__)
dirImg = os.path.join(dirPrincipal, 'img')

# Configuração da tela
larguraTela, alturaTela = 800, 600
tela = pygame.display.set_mode((larguraTela, alturaTela))
pygame.display.set_caption('WOP - Warrior Of Poá')

# Cores
branco = (255, 255, 255)
vermelho = (255, 0, 0)

# Utilizados na manipulação da spritesheet do player
larguraPlSs = 64 #PlSs = PlayerSpritesheet
alturaPlSs = 64
playerSpritesheet = pygame.image.load(os.path.join(dirImg, 'personagem_cespada.png')).convert_alpha()

import pygame

# Classe que herda de pygame.sprite.Sprite
class Player(pygame.sprite.Sprite):
    def __init__(self, sprite_sheet):
        super().__init__()  # Chama o inicializador da classe pai
        self.sheet = sprite_sheet
        self.image = pygame.Surface((32, 32), pygame.SRCALPHA)  # A imagem inicial
        self.rect = self.image.get_rect()  # Obtém o retângulo da imagem para movimentação
        

        self.speed = 2  # Velocidade de movimento
        self.posX = 400  # Posição inicial
        self.posY = 300
        self.rect.topleft = (self.posX, self.posY)  # Define a posição inicial

        self.frame_count = 0  # Contador de frames
        self.sprite_atual = 0  # Contador para alternar entre sprites de animação
        self.direction = 'DOWN'  # Direção de movimento (cima, baixo, esquerda, direita)

        self.frame_change = 10 #Quantidade de frames até a troca de sprite

        self.nova_direcao = False

        self.run = False

    def update(self):
        # Atualiza o contador de frames
        self.frame_count += 1
        self.moving = False

        if self.direction == 'UP'and self.run == False:
            self.sheet.action = 0
            self.rect.y -= self.speed  # Move para cima
            self.moving = True
        elif self.direction == 'DOWN'and self.run == False:
            self.sheet.action = 2
            self.rect.y += self.speed  # Move para baixo
            self.moving = True
        elif self.direction == 'LEFT'and self.run == False:
            self.sheet.action = 1
            self.rect.x -= self.speed  # Move para a esquerda
            self.moving = True
        elif self.direction == 'RIGHT'and self.run == False:
            self.sheet.action = 3
            self.rect.x += self.speed  # Move para a direita
            self.moving = True
        elif self.direction == 'UP'and self.run == True:
            self.sheet.action = 30
            self.rect.y -= self.speed  # Move para cima
            self.moving = True
        elif self.direction == 'DOWN'and self.run == True:
            self.sheet.action = 32
            self.rect.y += self.speed  # Move para baixo
            self.moving = True
        elif self.direction == 'LEFT'and self.run == True:
            self.sheet.action = 31
            self.rect.x -= self.speed  # Move para a esquerda
            self.moving = True
        elif self.direction == 'RIGHT'and self.run == True:
            self.sheet.action = 33
            self.rect.x += self.speed  # Move para a direita
            self.moving = True

            #self.sprite_atual = (self.sprite_atual + 1) % 2
        # A cada 10 frames, troca de sprite para evitar animação rápida demais
        if self.moving:
            if self.frame_count % self.frame_change == 0 or self.nova_direcao == True:  
                self.sheet.update()
                self.nova_direcao = False
        else:
            if self.sheet.action in [30,31,32,33]:
                self.sheet.tile_rect = self.sheet.cells[self.sheet.action-30][0]
            else:
                self.sheet.tile_rect = self.sheet.cells[self.sheet.action][0]

    def get_sprite(self):
        rect = pygame.Rect(self.sheet.tile_rect)
        sprite = pygame.Surface((32,32), pygame.SRCALPHA)
        sprite.blit(self.sheet.sheet, (0, 0), rect)

    def correr(self):
        if self.run:
            self.run = False
            self.speed = 2
            self.frame_change = 10

        elif self.run == False:
            self.run = True
            self.speed = 4
            self.frame_change = 5

        return self.run

# Criando o jogador e os grupos de sprites
player = Player(larguraTela//2, alturaTela//2)
todasSprites = pygame.sprite.Group(player)  # Criamos um grupo contendo o player
ataqueSprites = pygame.sprite.Group()  # Grupo para armazenar os ataques

# Loop principal
running = True
clock = pygame.time.Clock()

while running:
    tela.fill((0, 0, 0))  # Limpa a tela com a cor preta
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                ataque = player.ataque()
                if ataque:
                    ataqueSprites.add(ataque)  # Adiciona o ataque ao grupo de ataques

    # Atualiza os sprites
    todasSprites.update()
    ataqueSprites.update()

    # Desenha os sprites na tela
    todasSprites.draw(tela)
    ataqueSprites.draw(tela)

    pygame.display.flip()
    clock.tick(60)  # Controla a taxa de quadros

pygame.quit()