import pygame

class Set_graphics:
    def __init__(self, folder_path):
        self.folder_path = folder_path
    def set_graphics(self, obj, names):
        graphics = []
        for i in range(len(names)):
            path = self.folder_path + names[i]
            graphics.append(pygame.image.load(path).convert_alpha())
        obj.set_graphics(graphics)