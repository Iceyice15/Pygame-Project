# Pygame project

import pygame
import random
import time

# ----- CONSTANTS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
SKY_BLUE = (95, 165, 228)
WIDTH = 1280
HEIGHT = 720
TITLE = "Shinning Over You"


class Player(pygame.sprite.Sprite):
    def __init__(self, widht: int):
        """
        :param width: width of the rectangle in px

        """
        super().__init__()

        # Image
        self.image = pygame.Surface([width, width])
        # fill the image with an actual shape
        pygame.draw.circle(self.image,
                           YELLOW,
                           (width // 2, width // 2),  # draw in the middle
                           width // 2)  # double // makes it an integer

        self.image.set_colorkey(BLACK) # Make the edges transparent

        self.rect = self.image.rect()

def main():
    pygame.init()

    # ----- SCREEN PROPERTIES
    size = (WIDTH, HEIGHT)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption(TITLE)

    # ----- LOCAL VARIABLES
    done = False
    clock = pygame.time.Clock()

    # Create a player sprite group
    player = pygame.sprite.Group()

    # ----- MAIN LOOP
    while not done:
        # -- Event Handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        # ----- LOGIC

        # ----- RENDER
        screen.fill(BLACK)
        player.update()

        # Draw all the sprite groups
        player.draw(screen)

        # ----- UPDATE DISPLAY
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()