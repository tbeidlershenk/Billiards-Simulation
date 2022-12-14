import pygame
import math
import Config as cg
from Table import Table

class Game(object):

    def __init__(self):
        self.font = pygame.font.SysFont(cg.FONT, 30)
        self.screen = pygame.display.set_mode((cg.WIDTH, cg.HEIGHT))
        self.table_surface = Table()
        self.draw_game_components(0)
        self.game_paused = False

    def handle_events(self, events):

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                self.game_paused = not self.game_paused
            
            if self.game_paused:
                pass
            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.table_surface.is_stationary():
                        self.table_surface.cue.cue_hit(pygame.mouse.get_pos())
                    if event.key == pygame.K_r:
                        self.table_surface.table_balls = self.table_surface.setup_triangle() 
                if event.type == pygame.MOUSEMOTION:
                    print("drawing line")

    def draw_game_components(self, time):
        self.table_surface.draw(self.screen)
        self.table_surface.move_balls(self.screen, True, time)
        