import pygame
import os

# Inicializa o Pygame
pygame.init()

dirPrincipal = os.path.dirname(__file__)
dirImg = os.path.join(dirPrincipal, 'img')

# Configuração da tela
larguraTela, alturaTela = 800, 600
tela = pygame.display.set_mode((larguraTela, alturaTela))
pygame.display.set_caption('WOP - Warrior Of Poá')

# Cores
branco = (255, 255, 255)
vermelho = (255, 0, 0)

wopSpritesheet = pygame.image.load(os.path.join(dirImg, 'personagem_cespada.png')).convert_alpha

# Classe do jogador
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((40, 40))
        self.image.fill(branco)
        self.rect = self.image.get_rect(center=(x, y))
        self.atacando = False
        self.ataqueDuracao = 300  # Tempo de recarga entre ataques
        self.ataqueUltimoUso = 0

    def attack(self):
        if not self.atacando:
            self.atacando = True
            self.ataqueUltimoUso = pygame.time.get_ticks()  # Marca o tempo de ataque
            return Attack(self.rect.centerx, self.rect.centery)  # Cria o ataque
        return None

    def update(self):
        if self.atacando and pygame.time.get_ticks() - self.ataqueUltimoUso > self.ataqueDuracao:
            self.atacando = False  # Reseta o estado de ataque após a duração

# Classe do ataque (com animação)
class Attack(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.images = [pygame.Surface((50, 20)), pygame.Surface((60, 20)), pygame.Surface((70, 20))]
        for img in self.images:
            img.fill(vermelho)  # Preenche as imagens com vermelho (pode substituir por sprites)
        self.atual = 0  # Controla o frame atual da animação
        self.image = self.images[self.atual]
        self.rect = self.image.get_rect(center=(x + 30, y))  # Posição do ataque
        self.spawn_time = pygame.time.get_ticks()  # Marca o tempo em que o ataque foi criado
        self.animation_duration = 150  # Duração de cada frame da animação (em milissegundos)

    def update(self):
        # Atualiza o frame da animação após a duração definida
        if pygame.time.get_ticks() - self.spawn_time > self.animation_duration * (self.atual + 1):
            self.atual += 1
            if self.atual < len(self.images):
                self.image = self.images[self.atual]  # Troca para o próximo frame da animação
            else:
                self.kill()  # Remove o ataque após a animação ser concluída

# Criando o jogador e o grupo de ataques
player = Player(larguraTela//2, alturaTela//2)
attack_sprites = pygame.sprite.Group()  # Grupo para armazenar os ataques

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
                attack = player.attack()
                if attack:
                    attack_sprites.add(attack)  # Adiciona o ataque ao grupo de ataques

    # Atualiza o jogador e os ataques
    player.update()
    attack_sprites.update()

    # Desenha todos os sprites na tela
    player.update()
    attack_sprites.draw(tela)

    pygame.display.flip()
    clock.tick(60)  # Controla a taxa de quadros

pygame.quit()
