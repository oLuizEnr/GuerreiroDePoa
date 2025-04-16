import pygame
import math
from balas import Bala

class Personagem(pygame.sprite.Sprite):
    def __init__(self, sprite_sheet):
        super().__init__()
        self.sheet = sprite_sheet
        self.image = pygame.Surface((32, 32), pygame.SRCALPHA)
        self.rect = self.image.get_rect()

        self.collision_rect = self.rect.copy()
        
        self.bullet_img = pygame.image.load('bullet.png').convert_alpha()
        self.bullet_speed = 5
        
        self.atacando = False
        self.tempo_ataque = 0  # Contador de tempo para finalizar ataque
        self.duracao_ataque = 15  # Duração do ataque em frames
        
        self.HP = 10
        self.balas = pygame.sprite.Group()
        
        self.speed = 2  # Velocidade de movimento
        self.rect.topleft = (400, 300)
        
        self.frame_count = 0
        self.direction = 'DOWN'
        self.frame_change = 10
        self.nova_direcao = False
        
        self.run = False
        
        self.mouse_pos = (0, 0)
        
    def update(self, dialogo_open):
        if dialogo_open:
            return
        
        self.correr()  

        self.balas.update()
        self.frame_count += 1
        self.moving = False
        
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_w]:  # Cima
            self.rect.y -= self.speed
            self.collision_rect.y = self.rect.y  
            self.direction = 'UP'

        if keys[pygame.K_s]:  # Baixo
            self.rect.y += self.speed
            self.collision_rect.y = self.rect.y  
            self.direction = 'DOWN'

        if keys[pygame.K_a]:  # Esquerda
            self.rect.x -= self.speed
            self.collision_rect.x = self.rect.x  
            self.direction = 'LEFT'

        if keys[pygame.K_d]:  # Direita
            self.rect.x += self.speed
            self.collision_rect.x = self.rect.x  
            self.direction = 'RIGHT'

        self._atualizar_sprite()

    def correr(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LSHIFT]:  # Se Shift estiver pressionado
            self.speed = 4  # Velocidade aumentada
        else:
            self.speed = 2  # Velocidade normal

    def atacar(self):
        if self.atacando:
            return
        
        self.atacando = True
        self.tempo_ataque = 0
        
        angulo = self._calcular_angulo_ataque()
        self._definir_animacao_ataque(angulo)
        
        self.hitbox_ataque = self._criar_hitbox_ataque(angulo)
        
    def _calcular_angulo_ataque(self):
        rel_x, rel_y = self.mouse_pos[0] - self.rect.centerx, self.mouse_pos[1] - self.rect.centery
        return math.atan2(rel_y, rel_x)
    
    def _definir_animacao_ataque(self, angulo):
        if self.atacando:
            if self.sheet.action in [55, 56, 57, 58]:  # Se for ataque corpo a corpo
                self.sheet.tile_rect = pygame.Rect(self.sheet.tile_rect.x, self.sheet.tile_rect.y, 128, 128)  # Aumenta a captura
            else:
                self.sheet.tile_rect = self.sheet.cells[self.sheet.action][0]  # Normal

        if -math.pi / 4 <= angulo < math.pi / 4:
            self.sheet.action = 58  # Direita
        elif angulo >= 3 * math.pi / 4 or angulo < -3 * math.pi / 4:
            self.sheet.action = 56  # Esquerda
        elif math.pi / 4 <= angulo < 3 * math.pi / 4:
            self.sheet.action = 57  # Baixo
        else:
            self.sheet.action = 55  # Cima
    
    def _criar_hitbox_ataque(self, angulo):
        hitbox = pygame.Rect(self.rect.centerx, self.rect.centery, 40, 40)
        hitbox.fill((255,0,0))
        if self.sheet.action == 11:
            hitbox.x += 20
        elif self.sheet.action == 9:
            hitbox.x -= 20
        elif self.sheet.action == 10:
            hitbox.y += 20
        else:
            hitbox.y -= 20
        return hitbox
    
    def draw_balas(self, screen, camera):
        for bala in self.balas:
            screen.blit(self.bullet_img, camera.apply(bala))

    def _atualizar_sprite(self):
        if self.atacando:
            if self.frame_count % self.frame_change == 0:
                self.sheet.update()
        else:
            if self.direction == 'UP':
                self.sheet.action = 0  # ID da animação para cima
            elif self.direction == 'DOWN':
                self.sheet.action = 2  # ID da animação para baixo
            elif self.direction == 'LEFT':
                self.sheet.action = 1  # ID da animação para esquerda
            elif self.direction == 'RIGHT':
                self.sheet.action = 3  # ID da animação para direita

            if self.frame_count % self.frame_change == 0 or self.nova_direcao:
                self.sheet.update()
                self.nova_direcao = False
