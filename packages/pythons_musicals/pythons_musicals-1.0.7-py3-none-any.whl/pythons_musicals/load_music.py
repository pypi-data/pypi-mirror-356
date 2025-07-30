import pygame

class load():
    """Этот класс загружает музыку.
В аргументы надо ввести путь к файлу"""
    def __init__(self, directory):
        pygame.init()
        self.directory = directory
        self.sound = pygame.mixer.Sound(directory)

    def start(self):
        self.sound.play()
