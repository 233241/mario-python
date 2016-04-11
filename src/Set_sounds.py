import pygame

class Set_sounds:
    def __init__(self, music_folder_path, sounds_folder_path):
        self.music_folder_path = music_folder_path
        self.sounds_folder_path = sounds_folder_path
    def set_music_path(self, name):
        return self.music_folder_path + name
    def set_sound(self, name):
        path = self.sounds_folder_path + name
        return pygame.mixer.Sound(path)