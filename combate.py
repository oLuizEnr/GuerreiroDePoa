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

# Classe do player
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.animaRespiracao = []
        for i in range(2):
            self.animaRespiracao.append(playerSpritesheet.subsurface((i*larguraPlSs,24*alturaPlSs),(larguraPlSs,alturaPlSs)))
        self.atual = 0
        self.image = self.animaRespiracao[self.atual]
        self.rect = self.image.get_rect(center=(x, y))
        self.andando = False
        self.dashando = False
        self.dashDuracao = 300
        self.dashUltimoUso = 0
        self.atacando = False
        self.ataqueDuracao = 300 # Tempo de recarga entre ataques
        self.ataqueUltimoUso = 0
    
    def dash(self):
        if not self.dashando:
            self.dashando = True
            self.dashUltimoUso = pygame.time.get_ticks() # Marca o tempo de ataque
            return Dash(self.rect.centerx, self.rect.centery)  # Instancia o dash
        return None

    def ataque(self):
        if not self.atacando:
            self.atacando = True
            self.ataqueUltimoUso = pygame.time.get_ticks()
            return Attack(self.rect.centerx, self.rect.centery) # Cria o ataque
        return None

    def update(self):
        if not self.atacando:  # Se não estiver atacando, animação de respiração
            self.atual += 0.05  # Alterna lentamente entre os frames
            if self.atual >= len(self.animaRespiracao):
                self.atual = 0
            self.image = self.animaRespiracao[int(self.atual)]

        if self.atacando and pygame.time.get_ticks() - self.ataqueUltimoUso > self.ataqueDuracao:
            self.atacando = False  # Reseta o estado de ataque após a duração

class Dash(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

# Classe do ataque (com animação)
class Attack(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.animaAtaque = []
        for i in range(6):
            self.animaAtaque.append(playerSpritesheet.subsurface((i*128,29*128),(128,128)))
        self.atual = 0
        self.image = self.animaAtaque[self.atual]
        self.rect = self.image.get_rect(center=(x, y))
        self.spawn_time = pygame.time.get_ticks()  # Marca o tempo em que o ataque foi criado
        self.animation_duration = 150  # Duração de cada frame da animação (em milissegundos)

    def update(self):
        # # Atualiza o frame da animação após a duração definida
        # if pygame.time.get_ticks() - self.spawn_time > self.animation_duration * (self.atual + 1):
        #     self.atual += 1
        #     if self.atual < len(self.images):
        #         self.image = self.images[self.atual]  # Troca para o próximo frame da animação
        #     else:
        #         self.kill()  # Remove o ataque após a animação ser concluída
        self.atual += 0.10  # Alterna lentamente entre os frames
        if self.atual >= len(self.animaAtaque):
            self.atual = 0
        self.image = self.animaAtaque[int(self.atual)]

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