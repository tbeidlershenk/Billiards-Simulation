import pygame
import Config as cg

class SideScreen(object):

    def __init__(self, width, height, font):

        self.font = font
        self.width = width
        self.height = height

        self.surface = pygame.Surface((self.width, self.height))
        self.paused_message = self.font.render('Game Paused', self.surface, 'Blue')

    def draw(self, screen, game_paused):
        self.surface.fill('Grey')
        if game_paused:
            self.surface.blit(self.paused_message, (35,cg.HEIGHT-50))

        screen.blit(self.surface, (cg.WIDTH, 0))
        pass

