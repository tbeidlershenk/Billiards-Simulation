import Config as cg
import math
import pygame

class Pocket(object):

    def __init__(self, is_side_pocket, x, y):
        self.pos = (x,y)
        self.is_side_pocket = is_side_pocket
        if is_side_pocket:
            self.radius = cg.SIDE_POCKET_RADIUS
        else:
            self.radius = cg.POCKET_RADIUS

    def has_ball_collided(self, ball):
        if math.dist(self.pos, ball.pos) < self.radius + ball.radius:
            return True
        return False

    def draw(self, screen):
        rad = int(self.radius)
        pygame.draw.circle(screen, 'BLACK', (self.pos[0], self.pos[1]), rad)
