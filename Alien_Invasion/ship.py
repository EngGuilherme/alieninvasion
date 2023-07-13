
import pygame
from pygame.sprite import Sprite

class Ship(Sprite):

    def __init__(self, ai_settings, screen):
        """Inicializa a espaçonave e define sua posição inicial."""
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        #Carrega a imagem da espaçonave e obtém seu rect (retângulo)
        self.image = pygame.image.load('Alien_Invasion/images/ship.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        #Inicia cada nova espaconave na parte inferior central da tela
        self.rect.midbottom = self.screen_rect.midbottom

        #Armazena um valor decimal para o centro da espaçonave
        self.centerx = float(self.rect.centerx)
        self.centery = float(self.rect.centery)


         #Flags de movimento:
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        """Atualiza a posição da espaçonave de acordo com a flag de movimento"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.centerx += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left >0:
            self.centerx -= self.ai_settings.ship_speed_factor
        if self.moving_up and self.rect.top > 0:
            self.centery -= self.ai_settings.ship_speed_factor
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.centery += self.ai_settings.ship_speed_factor
        
        #Atualiza o objeto rect de acordo com self.center
        self.rect.centerx = self.centerx
        self.rect.centery = self.centery


    def blitme(self):
        """Desenha a espaçonave em sua posição atual."""
        self.screen.blit(self.image, self.rect)
    

    def center_ship(self):
        #Inicia cada nova espaconave na parte inferior central da tela
        self.rect.midbottom = self.screen_rect.midbottom

        #Armazena um valor decimal para o centro da espaçonave
        self.centerx = float(self.rect.centerx)
        self.centery = float(self.rect.centery)