import pygame
import sys
import json
import os
import math

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from spritesheet import SpriteSheet
from personagem import Personagem

# Animation action constants (adjust according to your spritesheet)
WALK_UP = 0
WALK_LEFT = 1
WALK_DOWN = 2
WALK_RIGHT = 3
RUN_UP = 4
RUN_LEFT = 5
RUN_DOWN = 6
RUN_RIGHT = 7
ATTACK_UP = 8
ATTACK_LEFT = 9
ATTACK_DOWN = 10
ATTACK_RIGHT = 11
BOW_UP = 12
BOW_LEFT = 13
BOW_DOWN = 14
BOW_RIGHT = 15

def inicio():
    global pause
    pygame.init()
    
    # Screen settings
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Jogo com Mapa e Colisões")

    # Get file paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    map_path = os.path.join(current_dir, 'map.json')
    spritesheet_path = os.path.join(current_dir, 'spritesheet.png')

    # Load map JSON
    try:
        with open(map_path, 'r') as f:
            map_data = json.load(f)
    except Exception as e:
        print(f"Erro ao carregar mapa: {e}")
        pygame.quit()
        sys.exit()

    # Map settings
    TILE_SIZE = map_data['tileSize']
    MAP_WIDTH = map_data['mapWidth']
    MAP_HEIGHT = map_data['mapHeight']

    class MapSpriteSheet:
        def __init__(self, filename):
            try:
                self.sheet = pygame.image.load(filename).convert_alpha()
            except Exception as e:
                print(f"Erro ao carregar spritesheet: {e}")
                self.sheet = None
        
        def get_sprite(self, x, y, width, height):
            if self.sheet:
                sprite = pygame.Surface((width, height), pygame.SRCALPHA)
                sprite.blit(self.sheet, (0, 0), (x, y, width, height))
                return sprite
            return None

    map_spritesheet = MapSpriteSheet(spritesheet_path)
    if map_spritesheet.sheet is None:
        pygame.quit()
        sys.exit()

    # Tile mapping
    TILE_MAPPING = {
        '33': (64, 256),
        '0': (0, 0), '1': (64, 0), '2': (128, 0),
        # ... (keep your existing tile mappings)
    }

    # Process map functions (keep your existing implementations)
    def process_map_for_collision(map_data):
        walls = []
        for layer in map_data['layers']:
            if layer['collider']:
                for tile in layer['tiles']:
                    x = int(tile['x']) * TILE_SIZE
                    y = int(tile['y']) * TILE_SIZE
                    walls.append(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))
        return walls

    def process_map_for_rendering(map_data):
        tiles = []
        layer_order = ['Background', 'Sand', 'pedras_para_preencher_vazio', 'Grass']
        # ... (keep your existing implementation)
        return tiles

    walls = process_map_for_collision(map_data)
    map_tiles = process_map_for_rendering(map_data)
    
    # Player sprite initialization with mixed sizes
    lista_acoes = [9, 9, 9, 9,   # Walk animations (64x64)
                   13, 13, 13, 13, # Run animations (64x64)
                   8, 8, 8, 8,    # Sword attacks (128x128)
                   6, 6, 6, 6]     # Bow attacks (128x128)

    lista_tamanhos = [(64,64) for _ in range(8)] + [(128,128) for _ in range(8)]

    try:
        player_sprite_path = os.path.join(current_dir, '..', '..', 'wopEspadachim.png')
        player_sprite = SpriteSheet(player_sprite_path, 0, 522, lista_acoes, lista_tamanhos, (0, 0, 0))
        player = Personagem(player_sprite)
    except Exception as e:
        print(f"Erro ao carregar sprite do jogador: {e}")
        pygame.quit()
        sys.exit()

    # Position player
    player.rect.x = 5 * TILE_SIZE
    player.rect.y = 5 * TILE_SIZE

    # Camera setup
    camera = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

    # Game setup
    clock = pygame.time.Clock()
    running = True
    pause = False
    DEBUG_MODE = True

    # Load other assets
    imagem_inimigo = pygame.image.load('Biomech Dragon Splice.png')
    vida_imagem = pygame.image.load('love-always-wins(1).png')
    interagir_bg = pygame.image.load("caixa_dialogo_pequena.jpg")
    omori = pygame.image.load('frente.png')

    # Create sprite groups
    inimigos = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    npcs = pygame.sprite.Group()

    # Add player
    all_sprites.add(player)
    player_group.add(player)

    # Add NPC
    npc = NPC(omori, screen)
    all_sprites.add(npc)
    npcs.add(npc)

    # Game loop
    while running:
        dialogo_a_abrir = False
        screen.fill((100, 100, 100))

        # Handle dialog
        dialogo_hitbox = pygame.sprite.groupcollide(player_group, npcs, False, False)
        if dialogo_hitbox:
            for jogador, dialogo in dialogo_hitbox.items():
                dialogo_a_abrir = dialogo[0].dialogo

        # Handle input
        click = pygame.mouse.get_pressed()[0]
        mouse_pos = pygame.mouse.get_pos()
        
        if click:
            if player.arcoEquipado:
                player.atacando = True
                player.hold_arrow(mouse_pos)
            else:
                player.sword_attack(mouse_pos)
                if DEBUG_MODE:
                    pygame.draw.rect(screen, (255,0,0), player.sword_hitbox, 2)
        else:
            player.atacando = False

        clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT:
                    player.correr()
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_1:
                    player.arcoEquipado = False
                if event.key == pygame.K_2:
                    player.arcoEquipado = True
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_z:
                    DEBUG_MODE = not DEBUG_MODE
                if event.key == pygame.K_SPACE and dialogo_a_abrir:
                    dialogo_a_abrir.trocar_texto()

        # Movement handling
        keys = pygame.key.get_pressed()
        player.direction = None
        if keys[pygame.K_w]:
            player.direction = 'UP'
        elif keys[pygame.K_s]:
            player.direction = 'DOWN'
        elif keys[pygame.K_a]:
            player.direction = 'LEFT'
        elif keys[pygame.K_d]:
            player.direction = 'RIGHT'

        # Update player
        old_x, old_y = player.rect.x, player.rect.y
        player.update(pause)

        # Collision detection
        for wall in walls:
            if player.collision_rect.colliderect(wall):
                player.rect.x, player.rect.y = old_x, old_y
                break
                
        # Update camera
        camera.center = player.rect.center
        camera.left = max(0, camera.left)
        camera.top = max(0, camera.top)
        camera.right = min(MAP_WIDTH * TILE_SIZE, camera.right)
        camera.bottom = min(MAP_HEIGHT * TILE_SIZE, camera.bottom)
        
        # Rendering
        screen.fill((0, 0, 0))
        
        # Draw map tiles
        for x, y, image in map_tiles:
            if (camera.left - TILE_SIZE <= x < camera.right and 
                camera.top - TILE_SIZE <= y < camera.bottom):
                screen.blit(image, (x - camera.left, y - camera.top))

        # Debug drawing
        if DEBUG_MODE:
            # Draw collision walls
            for wall in walls:
                if camera.colliderect(wall):
                    debug_wall_rect = pygame.Rect(
                        wall.x - camera.left,
                        wall.y - camera.top,
                        wall.width,
                        wall.height
                    )
                    pygame.draw.rect(screen, (255, 0, 0), debug_wall_rect, 1)
            
            # Draw player collision box
            debug_player_rect = pygame.Rect(
                player.rect.x - camera.left,
                player.rect.y - camera.top,
                player.rect.width,
                player.rect.height
            )
            pygame.draw.rect(screen, (0, 0, 255), debug_player_rect, 2)
            
            # Debug info
            font = pygame.font.SysFont(None, 24)
            debug_info = [
                f"Posição: ({player.rect.x}, {player.rect.y})",
                f"Direção: {player.direction}",
                f"Ataque: {'Sim' if player.atacando else 'Não'}",
                f"Arma: {'Arco' if player.arcoEquipado else 'Espada'}",
                "Z: Debug ON/OFF"
            ]
            
            for i, text in enumerate(debug_info):
                text_surface = font.render(text, True, (255, 255, 255))
                screen.blit(text_surface, (10, 10 + i * 25))

        # Draw player
        player.sheet.draw(screen, player.rect.x - camera.left, player.rect.y - camera.top)
        screen.blit(npc.image, (npc.rect.x - camera.left, npc.rect.y - camera.top))

        # Draw HP
        for vida in range(player.HP):
            screen.blit(vida_imagem, (18 + 32*vida, 0))
        
        # Draw dialog prompt
        if dialogo_a_abrir and dialogo_a_abrir.texto_open == False:
            font = pygame.font.Font(None, 48)
            render = font.render("Interagir", True, (0,0,0))
            screen.blit(interagir_bg, (300, 450))
            screen.blit(render, (325, 457))
            
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    inicio()