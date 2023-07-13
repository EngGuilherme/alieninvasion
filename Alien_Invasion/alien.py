
from typing import Any
import pygame
from pygame.sprite import Sprite
from random import randint

class Alien(Sprite):
    """Classe para representar um único alien na frota"""

    def __init__(self, ai_settings, screen):
        """Inicializa o alien e define sua posição inicial"""
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Carrega a imagem do alien e define seu retangulo
        aleatory_alien = [
            (pygame.image.load('Alien_Invasion/images/ufo_1.png')),
            (pygame.image.load('Alien_Invasion/images/ufo_2.png')),
            (pygame.image.load('Alien_Invasion/images/ufo_3.png')),
            (pygame.image.load('Alien_Invasion/images/ufo_4.png'))
            ]
        self.image = aleatory_alien[randint(0,3)]
        self.rect = self.image.get_rect()

        #Inicializa cada alienigena novo perto do canto superior esquerdo da tela
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        #Armazena a posição horizontal exata do alienigena
        self.x = float(self.rect.x)

    
    def check_edges(self):
        """Devolve True se o alien estiver na borda da tela"""
        screen_rect = self.screen.get_rect()
        if (self.rect.right >= screen_rect.right) or (self.rect.left <= 0):
            return True


    def update(self):
        """Move o alien para a direita"""
        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x


    def blitme(self):
        """Desenha o alien na posição atual"""
        self.screen.blit(self.image, self.rect)

