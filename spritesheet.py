import pygame

class SpriteSheet:
    def __init__(self, filename, pos_x, pos_y, lista_acoes, lista_tamanhos, color_key=None):
        """
        Modified SpriteSheet class to handle different sprite sizes
        
        Parameters:
        filename (str): Path to the spritesheet file
        pos_x (int): Initial X position of first sprite
        pos_y (int): Initial Y position of first sprite
        lista_acoes (list): List of frame counts for each action
        lista_tamanhos (list): List of (width, height) tuples for each action
        color_key (tuple, optional): Transparency color (R, G, B)
        """
        self.sheet = pygame.image.load(filename)
        self.lista_acoes = lista_acoes
        self.lista_tamanhos = lista_tamanhos
        self.action = 0
        self.cells = []
        self.index = 0
        
        if color_key:
            self.sheet = self.sheet.convert()
            self.sheet.set_colorkey(color_key)
        else:
            self.sheet = self.sheet.convert_alpha()
        
        # Create rectangles for each frame of each action
        current_y = pos_y
        for i, (action_frames, (width, height)) in enumerate(zip(lista_acoes, lista_tamanhos)):
            action_frames_list = []
            for frame in range(action_frames):
                rect = (pos_x + width * frame, current_y, width, height)
                action_frames_list.append(rect)
            self.cells.append(action_frames_list)
            current_y += height  # Move down for next action row
    
    def update(self):
        """ Update the current animation frame """
        if self.index < len(self.cells[self.action]) - 1:
            self.index += 1
        else:
            self.index = 0  # Or keep at last frame if you want to hold it
        self.tile_rect = self.cells[self.action][self.index]
    
    def draw(self, surface, x, y):
        """ Draw the current sprite at the specified position """
        rect = pygame.Rect(self.tile_rect)
        # Adjust position based on sprite size (center larger sprites properly)
        draw_x = x - (rect.width - 64) // 2 if rect.width > 64 else x
        draw_y = y - (rect.height - 64) // 2 if rect.height > 64 else y
        surface.blit(self.sheet, (draw_x, draw_y), self.tile_rect)