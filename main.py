import pygame
import sys
import math
import random

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Bobbing Ball')

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
color_list = [RED, BLUE, GREEN]

# Circle properties
circle_center = (WIDTH // 2, HEIGHT // 2)
circle_radius = 200
circle_color = BLACK

# Ball properties
ball_radius = 20
adjustment_list = list(range(-20, 21))  

class Ball:
    def __init__(self, pos, speed, color):
        self.pos = pos
        self.speed = speed
        self.color = color

    def move(self):
        self.pos[0] += self.speed[0]
        self.pos[1] += self.speed[1]

    def reflect(self, normal):
        self.speed = reflect_vector(self.speed, normal)

    def change_color(self, adjustment):
        self.color = add_tuples(self.color, adjustment)

    def draw(self, window):
        pygame.draw.circle(window, self.color, (int(self.pos[0]), int(self.pos[1])), ball_radius)

def is_inside_circle(pos, center, radius):
    return math.sqrt((pos[0] - center[0])**2 + (pos[1] - center[1])**2) < radius

def reflect_vector(velocity, normal):
    normal_length = math.sqrt(normal[0]**2 + normal[1]**2)
    if normal_length == 0:
        return velocity
    # Normalize the normal vector
    normal = [normal[0] / normal_length, normal[1] / normal_length]
    # Reflect the velocity
    dot_product = 2 * (velocity[0] * normal[0] + velocity[1] * normal[1])
    reflection = [velocity[0] - dot_product * normal[0], velocity[1] - dot_product * normal[1]]
    return reflection

def add_tuples(t1, t2):
    return tuple(min(max(a + b, 0), 255) for a, b in zip(t1, t2))

def subtract_tuples(t1, t2):
    return tuple(min(max(a - b, 0), 255) for a, b in zip(t1, t2))

def hit(ball, circle_center, circle_radius):

    if not is_inside_circle(ball.pos, circle_center, circle_radius - ball_radius):

        # Calculate normal vector
        normal = [ball.pos[0] - circle_center[0], ball.pos[1] - circle_center[1]]
        
        # Reflect the ball speed
        ball.reflect(normal)
        
        # Move the ball back inside the boundary
        ball.pos[0] += ball.speed[0]
        ball.pos[1] += ball.speed[1]
        
        # Change colors
        adjustment = (random.choice(adjustment_list), random.choice(adjustment_list), random.choice(adjustment_list))
        ball.change_color(adjustment)
        
        # Return new circle color and create a new ball
        new_ball = Ball(
            pos=[circle_center[0], circle_center[1] - circle_radius + ball_radius],
            speed=[-2, 2],
            color=random.choice(color_list)
        )
        print ("ball in hit func" + str(type(new_ball)))
        return new_ball , type(new_ball)
    
    return None, None

# Initialize the ball list
ball_list = [Ball(
    pos=[circle_center[0] + 10, circle_center[1] - circle_radius + ball_radius],
    speed=[1, 5],
    color=(100, 50, 75)
)]

# Clock
clock = pygame.time.Clock()

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Check collision and update ball list
    # new_balls = []
    # for ball in ball_list:
        # new_ball = hit(ball, circle_center, circle_radius)
    #     if new_ball:
    #         # new_balls.append((new_ball))
    #         ball_list.append(new_ball)
    #         print(ball_list)
    
    # Add new balls to the list
    # ball_list.extend(new_balls)

    # Move and draw balls
    window.fill(WHITE)
    pygame.draw.circle(window, BLACK, circle_center, circle_radius, 2)
    
    print("ball list" )
    print(ball_list)
    # for i in range(0,1) :
    #     ball = ball_list[i]

    print('outside of ball list')
    for ball in ball_list:
        # print('inside of')
        # print(ball)
        ball.move()
        ball.draw(window)
       
       
        new_ball  , t = hit(ball, circle_center, circle_radius)
        print (t)
        # print ("ball in main loop" + str(type(new_ball)))
        # new_ball.move()
        # if new_ball:

        #     new_ball.move()
            # print("end of main func" + str(type(new_ball)))
            # ball_list.append(new_ball)
            
            # print('ball list : ')
            # print(ball_list)
        
    
    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

pygame.quit()
sys.exit()
