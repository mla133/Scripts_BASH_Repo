# Pygame development 1-3

# Gain access to pygame library and initialize it
import pygame
pygame.init()

# Size of screen
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400
SCREEN_TITLE = 'Cross RPG'

player_image = pygame.image.load('player.png')

# Scale up the player image (which is 12x16 normally)
player_image = pygame.transform.scale(player_image, (50, 50))

# Define colors according to RGB codes
WHITE_COLOR = (255, 255, 255)
BLACK_COLOR = (0, 0, 0)


# Clock used to update game events and frames
clock = pygame.time.Clock()
# Typical rate of 60, equivalent to FPS
TICK_RATE = 60
is_game_over = False
# Create the window of specified size in white to display the game
game_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Set the game window color to white
game_screen.fill(WHITE_COLOR)
pygame.display.set_caption(SCREEN_TITLE)

# Main game loop, used to update all gameplay such as movement, checks, and graphics
# Runs until is_game_over = True
while not is_game_over:

    # A loop to get all of the events occurring at any given time
    # Events are most often mouse movement, clicks, exit events
    for event in pygame.event.get():
        # If we have a quit type event (exit out), then exit out of game loop
        if event.type == pygame.QUIT:
            is_game_over = True

        print(event)

    # Draw a rectangle on top of the game screen canvas (x, y, height, width
    # pygame.draw.rect(game_screen, BLACK_COLOR, [150, 150, 100, 100])
    # Draw a circle on top of the game screen (x, y, radius)
    # pygame.draw.circle(game_screen, BLACK_COLOR, (200, 100), 50)

    # Draw the player image on top of the game screen at (x, y) position
    game_screen.blit(player_image, (175, 175))
    
    # Update all game graphics
    pygame.display.update()
    # Tick the clock to update everything within the game
    clock.tick(TICK_RATE)

# Quit pygame and the program
pygame.quit()
quit()
