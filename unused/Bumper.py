import math
import Config as cg

class Bumper(object):

    def __init__(self, is_side_bumper, x, y, width, height):
        self.is_side_bumper = is_side_bumper
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.area = width * height
        self.corner_points = [
            (x,y),
            (x+width, y),
            (x+width, y+height),
            (x, y+height)
        ]
        self.bounding_points = [
            (x - cg.RADIUS,y - cg.RADIUS),
            (x + width - cg.RADIUS,y + height - cg.RADIUS),
            (x + width + cg.RADIUS, y + height + cg.RADIUS),
            (x + cg.RADIUS, y+height + cg.RADIUS)
        ]


    def has_collided(self, ball):
        bounded_area = (self.width + 2*ball.radius) * (self.height + 2*ball.radius)
        sum_area = self.calc_triangle_area(ball.pos, self.bounding_points[0], self.bounding_points[1])
        print(sum_area)
        sum_area += self.calc_triangle_area(ball.pos, self.bounding_points[1], self.bounding_points[2])        
        print(sum_area)

        sum_area += self.calc_triangle_area(ball.pos, self.bounding_points[2], self.bounding_points[3])
        print(sum_area)

        sum_area += self.calc_triangle_area(ball.pos, self.bounding_points[3], self.bounding_points[0])

        if (sum_area > bounded_area):
            print('sum='+str(sum_area))
            print('rec='+str(bounded_area))
            pass
        else:

            self.handle_collision(ball)



        

    def handle_collision(self, ball):
        print('collision')
        if self.is_side_bumper:
            ball.vel = (-1 * ball.vel[0] * cg.CONST_RESTITUTION_RAIL, ball.vel[1] * cg.CONST_RESTITUTION_RAIL)
        else:
            ball.vel = (ball.vel[0] * cg.CONST_RESTITUTION_RAIL, -1 * ball.vel[1] * cg.CONST_RESTITUTION_RAIL)



    def calc_triangle_area(self, p1, p2, p3):
        base = math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)
        midpoint = ((p1[0] + p2[0])/2, (p1[1] + p2[1])/2)
        height = math.sqrt((p3[0]-midpoint[0])**2 + (p3[1]-midpoint[1])**2)
        area = 0.5 * base * height
        #print(area)
        return area

