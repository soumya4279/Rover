import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
ROVER_SIZE = 20
ROVER_COLOR = (0, 128, 255)
BACKGROUND_COLOR = (200, 200, 200)
GPS_SCALE = 0.1  # Scale for GPS coordinates to fit the screen

# Setup Display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("SIH Rover GPS Navigation")

# Rover Class
class Rover:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def draw(self):
        pygame.draw.rect(screen, ROVER_COLOR, (self.x, self.y, ROVER_SIZE, ROVER_SIZE))

    def get_gps_coordinates(self):
        # Convert screen coordinates to GPS-like coordinates
        return (self.x * GPS_SCALE, self.y * GPS_SCALE)

# Initialize Rover
rover = Rover(100, 100)

# Main loop
clock = pygame.time.Clock()

while True:
    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Input Handling
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        rover.move(-5, 0)
    if keys[pygame.K_RIGHT]:
        rover.move(5, 0)
    if keys[pygame.K_UP]:
        rover.move(0, -5)
    if keys[pygame.K_DOWN]:
        rover.move(0, 5)

    # Clear Screen
    screen.fill(BACKGROUND_COLOR)

    # Draw Rover
    rover.draw()

    # Print GPS Coordinates
    gps_coordinates = rover.get_gps_coordinates()
    print(f"GPS Coordinates: X={gps_coordinates[0]:.2f}, Y={gps_coordinates[1]:.2f}")

    # Update Display
    pygame.display.flip()
    clock.tick(30)
