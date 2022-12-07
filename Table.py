import pygame
import random
import math
import Config as cg
from Ball import Ball
from Pocket import Pocket

class Table(object):

    def __init__(self):
        self.side_width = int(cg.WIDTH * 0.055)
        self.table_dim = (cg.WIDTH - 2 * self.side_width, cg.HEIGHT - 2 * self.side_width)
        self.triangle_loc = (self.side_width + int( 3 * self.table_dim[0] / 4), self.side_width + int(self.table_dim[1] / 2))
        self.pool_table = pygame.image.load('files/pool_table.jpg').convert_alpha()
        self.pool_table = pygame.transform.scale(self.pool_table, (cg.WIDTH, cg.HEIGHT))
        self.table_balls = self.setup_triangle()
        self.pockets = self.setup_pockets()
        self.pocket_balls = []
        self.paused = False

    def draw(self, screen):
        screen.blit(self.pool_table, (0,0))

        # for pocket in self.pockets:
        #     pocket.draw(screen)

    def setup_triangle(self):
    
        self.cue = Ball(self, 200, cg.HEIGHT/2 + 25, 0, 0, 'White')
        table = [self.cue]
        spc = cg.TRIANGLE_SPACING
        
        for i in range(cg.TRIANGLE_SIZE):
            
            for j in range(i + 1):
                
                x = self.triangle_loc[0] + (i * spc)
                y = self.triangle_loc[1] + (i * spc) - (2 * j * spc)
                color = 'Blue'
                b = Ball(self, x, y, 0, 0, color)
                table.append(b)
                

        return table

    def setup_pockets(self):
        rad1 = cg.POCKET_RADIUS
        rad2 = cg.SIDE_POCKET_RADIUS
        width = cg.WIDTH
        height = cg.HEIGHT
        pockets = [
            Pocket(False, rad1, rad1),
            Pocket(True, .5 * width, rad2),
            Pocket(False, width - rad1, rad1),
            Pocket(False, rad1, height - rad1),
            Pocket(True, .5 * width, height - rad2),
            Pocket(False, width - rad1, height - rad1)
        ]
        return pockets


    def move_balls(self, screen, visible):
        for ball in self.table_balls:
            if visible:
                ball.draw(screen)
            if (ball.vel[0] != 0 or ball.vel[1] != 0):
                ball.physics_process(self.side_width, cg.DELTA)
            
            for other_ball in self.table_balls:
                if other_ball != ball:
                        ball.check_ball_collision(other_ball)
            
            self.check_pocket_collisions()

    def check_bumper_collision(self, ball, side_width):
        # y direc collision (top)
        in_left_x_range = ball.pos[0] >= cg.X_BUMPER_RANGES[0][0] and ball.pos[0] <= cg.X_BUMPER_RANGES[0][1]
        in_right_x_range = ball.pos[0] >= cg.X_BUMPER_RANGES[1][0] and ball.pos[0] <= cg.X_BUMPER_RANGES[1][1]
        ball_high = ball.pos[1] < side_width + ball.radius
        ball_moving_up = ball.vel[1] < 0
        ball_low = ball.pos[1] > cg.HEIGHT - side_width - ball.radius
        ball_moving_down = ball.vel[1] > 0
        ball_past_bumper = (ball_high and ball_moving_up) or (ball_low and ball_moving_down)

        if (in_left_x_range or in_right_x_range) and ball_past_bumper:
            ball.vel = (ball.vel[0], -1 * ball.vel[1])

        # x_direc_collision
        in_y_range = ball.pos[1] >= cg.Y_BUMPER_RANGES[0][0] and ball.pos[1] <= cg.Y_BUMPER_RANGES[0][1]
        ball_past_bumper = ball.pos[0] < side_width + ball.radius or ball.pos[0] > cg.WIDTH - side_width - ball.radius
        
        if in_y_range and ball_past_bumper:
            ball.vel = (-1 * ball.vel[0], ball.vel[1])

    def check_pocket_collisions(self):
        for ball in self.table_balls:
            for pocket in self.pockets:
                if pocket.has_ball_collided(ball):
                    self.table_balls.remove(ball)
                    self.pocket_balls.append(ball)

    def is_stationary(self):
        for ball in self.table_balls:
            if ball.vel[0] != 0 or ball.vel[1] != 0:
                return False

        return True

