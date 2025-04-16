import pygame
import math

class Personagem(pygame.sprite.Sprite):
    def __init__(self, sprite_sheet):
        super().__init__()
        self.sheet = sprite_sheet
        self.image = pygame.Surface((64, 64), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        
        self.bullet_img = pygame.image.load('bullet.png').convert_alpha()
        self.bullet_speed = 5
        self.sword_attackX = 0
        self.sword_attackY = 0
        self.offset = 64
        self.arcoEquipado = False
        self.atacando = False

        self.HP = 10
        self.balas = pygame.sprite.Group()
        self.speed = 2
        self.posX = 400
        self.posY = 300
        self.rect.center = (self.posX, self.posY)
        self.frame_count = 0
        self.sprite_atual = 0
        self.direction = 'DOWN'
        self.frame_change = 10
        self.nova_direcao = False
        self.run = False
        self.ivuln = False
        self.iframes = 90
        self.contador_iframes = 0
        self.dodge_iframes = 0
        self.mouse_pos = (0,0)
        self.mousex, self.mousey = self.mouse_pos
        self.center_x, self.center_y = 800 // 2, 600 // 2
        self.segurando = False
        
        # Attack animation properties
        self.attack_frame_duration = 5
        self.attack_frame_counter = 0
        self.attack_animation_playing = False
        self.sword_hitbox = pygame.Rect(0, 0, 128, 128)
        
    def update(self, dialogo_open):
        if dialogo_open:
            return
            
        self.balas.update(dialogo_open)
        self.frame_count += 1
        self.moving = False

        # Handle attack animation
        if self.attack_animation_playing:
            self.attack_frame_counter += 1
            if self.attack_frame_counter >= self.attack_frame_duration:
                self.attack_frame_counter = 0
                self.sheet.update()
                
                # Check if animation is complete
                if self.sheet.index == len(self.sheet.cells[self.sheet.action]) - 1:
                    self.attack_animation_playing = False
                    self.atacando = False
                    # Reset to normal sprite size action
                    if self.direction == 'UP':
                        self.sheet.action = 0
                    elif self.direction == 'LEFT':
                        self.sheet.action = 1
                    elif self.direction == 'DOWN':
                        self.sheet.action = 2
                    elif self.direction == 'RIGHT':
                        self.sheet.action = 3

        # Movement handling
        if not self.attack_animation_playing:
            if self.direction == 'UP' and not self.run:
                self.sheet.action = 0
                self.rect.y -= self.speed
                self.moving = True
            elif self.direction == 'DOWN' and not self.run:
                self.sheet.action = 2
                self.rect.y += self.speed
                self.moving = True
            elif self.direction == 'LEFT' and not self.run:
                self.sheet.action = 1
                self.rect.x -= self.speed
                self.moving = True
            elif self.direction == 'RIGHT' and not self.run:
                self.sheet.action = 3
                self.rect.x += self.speed
                self.moving = True
            elif self.direction == 'UP' and self.run:
                self.sheet.action = 30
                self.rect.y -= self.speed
                self.moving = True
            elif self.direction == 'DOWN' and self.run:
                self.sheet.action = 32
                self.rect.y += self.speed
                self.moving = True
            elif self.direction == 'LEFT' and self.run:
                self.sheet.action = 31
                self.rect.x -= self.speed
                self.moving = True
            elif self.direction == 'RIGHT' and self.run:
                self.sheet.action = 33
                self.rect.x += self.speed
                self.moving = True

        # Animation updates
        if self.moving:
            if self.frame_count % self.frame_change == 0 or self.nova_direcao:
                self.sheet.update()
                self.nova_direcao = False
        elif self.atacando:
            if self.frame_count % self.frame_change == 0:
                self.sheet.update()
        else:
            if self.sheet.action in [30,31,32,33]:
                self.sheet.tile_rect = self.sheet.cells[self.sheet.action-30][0]
            else:
                self.sheet.tile_rect = self.sheet.cells[self.sheet.action][0]

        # Update hitbox position for attacks
        if self.atacando and not self.arcoEquipado:
            if self.sheet.action == 48:  # Right attack
                self.sword_hitbox.midleft = self.rect.midright
            elif self.sheet.action == 45:  # Left attack
                self.sword_hitbox.midright = self.rect.midleft
            elif self.sheet.action == 47:  # Down attack
                self.sword_hitbox.midtop = self.rect.midbottom
            elif self.sheet.action == 46:  # Up attack
                self.sword_hitbox.midbottom = self.rect.midtop

        # Clean up bullets
        for bala in self.balas:
            if not bala.active:
                self.balas.remove(bala)

        self.collision_rect = self.rect.inflate(-40, -20)

    def sword_attack(self, mouse_pos):
        if not self.attack_animation_playing:
            self.atacando = True
            self.attack_animation_playing = True
            self.attack_frame_counter = 0
            self.sheet.index = 0
            
            self.mouse_pos = mouse_pos
            self.mousey = self.mouse_pos[1]
            self.mousex = self.mouse_pos[0]
            self.rel_x = self.mousex - self.center_x
            self.rel_y = self.mousey - self.center_y
            self.angle = math.atan2(self.rel_y, self.rel_x)
            
            # Set the appropriate attack action based on angle
            if -math.pi / 4 <= self.angle < math.pi / 4:
                self.sheet.action = 48  # Right attack (128x128)
            elif self.angle >= 3 * math.pi / 4 or self.angle < -3 * math.pi / 4:
                self.sheet.action = 45  # Left attack (128x128)
            elif math.pi / 4 <= self.angle < 3 * math.pi / 4:
                self.sheet.action = 47  # Down attack (128x128)
            else:
                self.sheet.action = 46  # Up attack (128x128)

    # ... (keep other methods the same)