import pygame
import sys
import math
import random

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 1000, 1000
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
circle_radius = 300

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

class Circle:
    def __init__(self, center, radius, color):
        self.center = center
        self.radius = radius
        self.color = color
    
    def change_color(self, adjustment):
        self.color = add_tuples(self.color, adjustment)
    
    def draw(self, window):
        pygame.draw.circle(window, self.color, self.center, self.radius, 2)

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

def hit(ball, circle):
    if not is_inside_circle(ball.pos, circle.center, circle.radius - ball_radius):
        # Calculate normal vector
        normal = [ball.pos[0] - circle.center[0], ball.pos[1] - circle.center[1]]
        
        # Reflect the ball speed
        ball.reflect(normal)
        
        # Move the ball back inside the boundary
        ball.pos[0] -= ball.speed[0]
        ball.pos[1] -= ball.speed[1]
        
        # Change colors
        adjustment = (random.choice(adjustment_list), random.choice(adjustment_list), random.choice(adjustment_list))
        ball.change_color(adjustment)
        circle.change_color(adjustment)

        
        # Add a smaller circle inside
        new_circle_radius = circle.radius + 5
        if new_circle_radius > 0:  # Ensure the new circle has a positive radius
            new_circle = Circle(
                center=[500,500],
                radius=new_circle_radius,
                color=random.choice(color_list)
            )
            return new_circle
    return None

ball = Ball(
    pos=[circle_center[0], circle_center[1]],  # Start at the circle center
    speed=[2, 2],  # Move towards the bottom-right initially
    color=(100, 50, 75)
)

# Initialize circle list
circle = Circle(circle_center, circle_radius, RED)
circle_list = [circle]

# Clock
clock = pygame.time.Clock()

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move ball
    ball.move()

    # Check for collisions and add new circles if needed
    for circle in circle_list:
        new_circle = hit(ball, circle)
        if new_circle:
            circle_list.append(new_circle)
    
    # Draw everything
    window.fill(WHITE)
    for circle in circle_list:
        circle.draw(window)
    ball.draw(window)
    
    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

pygame.quit()
sys.exit()
