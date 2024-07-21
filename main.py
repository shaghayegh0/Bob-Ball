import pygame
import sys
import math
import random

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Ball in Circle Game')

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
circle_color = BLUE

# Ball properties
ball_radius = 20
ball_pos = [circle_center[0] + 10, circle_center[1] - circle_radius + ball_radius]
ball_speed = [1, 5]
ball_color = (100, 50, 75)
adjustment_list = list(range(-20,20))
adjustment = (10,10,10)

# Clock
clock = pygame.time.Clock()

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

def hit(ball_pos, ball_speed, circle_center, circle_radius, ball_radius, ball_color, circle_color):
    if not is_inside_circle(ball_pos, circle_center, circle_radius - ball_radius):
        
        # Calculate normal vector
        normal = [ball_pos[0] - circle_center[0], ball_pos[1] - circle_center[1]]
        
        # Reflect the ball speed
        ball_speed = reflect_vector(ball_speed, normal)
        
        # Move the ball back inside the boundary
        ball_pos[0] += ball_speed[0]
        ball_pos[1] += ball_speed[1]
        
        # Change colors
        adjustment = (random.choice(adjustment_list) , random.choice(adjustment_list) , random.choice(adjustment_list))
        ball_color = add_tuples(ball_color, adjustment)
        circle_color = random.choice(color_list)
        print(ball_color)
    
    return ball_speed, ball_color, circle_color

def add_tuples(t1, t2):
    return tuple(min(max(a + b, 0), 255) for a, b in zip(t1, t2))

def subtract_tuples(t1, t2):
    return tuple(min(max(a - b, 0), 255) for a, b in zip(t1, t2))

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move the ball
    ball_pos[0] += ball_speed[0]
    ball_pos[1] += ball_speed[1]

    # Check collision with circle boundary and change colors if hit
    ball_speed, ball_color, circle_color = hit(ball_pos, ball_speed, circle_center, circle_radius, ball_radius, ball_color, circle_color)

    # Fill the background
    window.fill(WHITE)

    # Draw the circle boundary
    pygame.draw.circle(window, circle_color, circle_center, circle_radius, 2)

    # Draw the ball
    pygame.draw.circle(window, ball_color, ball_pos, ball_radius)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

pygame.quit()
sys.exit()
