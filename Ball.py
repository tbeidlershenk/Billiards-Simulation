import pygame
import math
import Config as cg

class Ball(object):
    
    def __init__(self, table, x, y, x_vel, y_vel, color):
        self.table = table
        self.pos = (x, y)
        self.radius = cg.RADIUS
        self.vel = (x_vel, y_vel)
        self.color = color
        self.mass = 10.0
        self.update_angle()
        self.update_acceleration(cg.DELTA)
        self.collision_occurred = False
        self.collision_log = []
        
    def draw(self, screen):
        rad = int(self.radius)
        pygame.draw.circle(screen, self.color, (self.pos[0], self.pos[1]), rad)

    def physics_process(self, side_width, delta):
        if (self.angle != None):
            self.update_position(delta)
            self.update_velocity(side_width, delta)
            self.update_acceleration(delta)
    
    def update_position(self, delta):
        
        new_x = self.pos[0] + self.vel[0]
        new_y = self.pos[1] + self.vel[1]
        self.pos = (new_x, new_y)

    def update_velocity(self, side_width, delta):
        
        self.table.check_bumper_collision(self, side_width)
        new_vx = self.vel[0] + self.accel[0] * delta
        new_vy = self.vel[1] + self.accel[1] * delta
        self.vel = (new_vx, new_vy)
        self.stop_oscillation()

    def update_acceleration(self, delta):
        force_friction = self.mass * cg.G * cg.FRICTION
        self.update_angle()
        accel = force_friction / self.mass
        self.accel = (accel * math.cos(self.angle), accel * math.sin(self.angle))

    def update_angle(self):
        try:
            ratio = self.vel[1] / self.vel[0]
            self.angle = math.atan(ratio)
        except:
            if (self.vel[1] >= 0):
                self.angle = math.pi/2
            else:
                self.angle = 3 * math.pi/2
        if (self.vel[0] < 0):
            self.angle += math.pi

    def stop_oscillation(self):
        low_vel = 0.1
        if (self.vel[0] < low_vel and self.vel[0] > -1 * low_vel):
            self.vel = (0, self.vel[1])
        if (self.vel[1] < low_vel and self.vel[1] > -1 * low_vel):
            self.vel = (self.vel[0], 0)
   
    def check_ball_collision(self, b2):
        circle_dist = math.sqrt((self.pos[0] - b2.pos[0]) ** 2 + (self.pos[1] - b2.pos[1]) ** 2)
        sum_radii = self.radius + b2.radius
        overlap_dist = sum_radii - circle_dist

        if (overlap_dist >= 0):
            # get collision point
            cx = min(self.pos[0], b2.pos[0]) + abs(self.pos[0] - b2.pos[0]) / 2
            cy = min(self.pos[1], b2.pos[1]) + abs(self.pos[1] - b2.pos[1]) / 2
            collision_point = (cx, cy)
            # move balls back
            self.handle_ball_collision(b2, collision_point, sum_radii, circle_dist)
            self.collision_log.append(b2)
        else:
            self.collision_log.append(None)

    def move_balls_back(self, b2, collision_point, sum_radii, circle_dist):
        
        step = 0.2
        opp_angle_c1 = self.angle - math.pi 
        opp_angle_c2 = b2.angle - math.pi
        while (circle_dist < sum_radii):
            if (self.vel == (0,0) and b2.vel == (0,0)):
                break
            if (self.vel[0] != 0 or self.vel[1] != 0):
                c1_new_x = self.pos[0] + step * math.cos(opp_angle_c1)
                c1_new_y = self.pos[1] + step * math.sin(opp_angle_c1)
                self.pos = (c1_new_x, c1_new_y)
            if (b2.vel[0] != 0 or b2.vel[1] != 0):
                c2_new_x = b2.pos[0] + step * math.cos(opp_angle_c2)
                c2_new_y = b2.pos[1] + step * math.sin(opp_angle_c2)
                b2.pos = (c2_new_x, c2_new_y)
            circle_dist = math.sqrt((self.pos[0] - b2.pos[0]) ** 2 + (self.pos[1] - b2.pos[1]) ** 2)
    
    def handle_ball_collision(self, b2, collision_point, sum_radii, circle_dist): 
        
        self.move_balls_back(b2, collision_point, sum_radii, circle_dist)

        mag_v1 = math.sqrt(self.vel[0] ** 2 + self.vel[1] ** 2)
        mag_v2 = math.sqrt(b2.vel[0] ** 2 + b2.vel[1] ** 2)

        sum_mass = self.mass + b2.mass
        contact_angle = 0
        try:
            contact_angle = math.atan((self.pos[1] - b2.pos[1]) / (self.pos[0] - b2.pos[0]))
        except:
            if (self.pos[1] - b2.pos[1] > 0):
                contact_angle = math.pi/2
            else:
                contact_angle = 3 * math.pi/2

        c1_frac = ((mag_v1 * math.cos(self.angle - contact_angle) * (self.mass - b2.mass))) + 2 * b2.mass * mag_v2 * math.cos(b2.angle - contact_angle) / sum_mass
        new_vel_x1 = c1_frac * math.cos(contact_angle) + (mag_v1 * math.sin(self.angle - contact_angle) * math.cos(contact_angle + math.pi/2))
        new_vel_y1 = c1_frac * math.sin(contact_angle) + (mag_v1 * math.sin(self.angle - contact_angle) * math.sin(contact_angle + math.pi/2))
        c2_frac = ((mag_v2 * math.cos(b2.angle - contact_angle) * (b2.mass - self.mass))) + 2 * self.mass * mag_v1 * math.cos(self.angle - contact_angle) / sum_mass        
        new_vel_x2 = c2_frac * math.cos(contact_angle) + (mag_v2 * math.sin(b2.angle - contact_angle) * math.cos(contact_angle + math.pi/2))
        new_vel_y2 = c2_frac * math.sin(contact_angle) + (mag_v2 * math.sin(b2.angle - contact_angle) * math.sin(contact_angle + math.pi/2))

        self.vel = (cg.CONST_RESTITUTION_BALL * new_vel_x1, cg.CONST_RESTITUTION_BALL * new_vel_y1)
        b2.vel = (cg.CONST_RESTITUTION_BALL * new_vel_x2, cg.CONST_RESTITUTION_BALL * new_vel_y2)

    def cue_hit(self, mouse_pos):
        cue_pos = (self.pos[0] + self.radius, self.pos[1] + self.radius)    
        dist = math.sqrt((self.pos[0] + self.radius - mouse_pos[0]) ** 2 + (self.pos[1] + self.radius - mouse_pos[1]) ** 2)
        angle = math.atan((cue_pos[1] - mouse_pos[1])/(cue_pos[0] - mouse_pos[0]))
        if (mouse_pos[0] < cue_pos[0]):
            angle += math.pi
        self.vel = ((dist/30) * math.cos(angle), (dist/30) * math.sin(angle))