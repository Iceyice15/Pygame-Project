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
ENEMY_VELOCITY = 10
NORMAL_ENEMY_HEALTH = 50
LIVES = 3
TITLE = "Shinning Over You"

# Create player class
def rot_center(image, angle, x, y):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(center=(x, y)).center)

    return rotated_image, new_rect


class Player(pygame.sprite.Sprite):
    def __init__(self):
        # """
        # :param width: width of the rectangle in px
        #
        # """
        super().__init__()

        # Image
        # self.image = pygame.Surface([width, width])
        # # fill the image with an actual shape
        # pygame.draw.rect(self.image,
        #                  YELLOW,
        #                  [WIDTH/2, 10, 400, 200])  # Draw a rectangle as the ray of sun

        self.image = pygame.image.load("./assets/sun.png")

        # Rect

        self.rect = self.image.get_rect()

        # Rotate player
        self.angle = 2

    def update(self, *args: Any, **kwargs: Any) -> None:
        self.image, self.rect = rot_center(self.image, self.angle, )


# Create enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Image
        self.image = pygame.image.load("./assets/butterfly_enemy.png")
        self.image = pygame.transform.scale(self.image, (38, 38))
        self.image.set_colorkey(WHITE)

        # Rect
        self.rect = self.image.get_rect()

        # self.xvel & self.yvel
        self.yvel = ENEMY_VELOCITY
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-250, -150)

    def update(self):
        self.rect.y += self.yvel


# Create protect class
class Protect(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Image
        self.image = pygame.image.load("./assets/normal_face.png")

        # Rect
        self.rect = self.image.get_rect()


def main():

    pygame.init()

    # ----- SCREEN PROPERTIES
    size = (WIDTH, HEIGHT)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption(TITLE)

    # ----- LOCAL VARIABLES
    done = False
    clock = pygame.time.Clock()
    num_enemy = 10
    score = 0
    default_font = pygame.font.SysFont("SERIF", 20)

    # Create sprite groups
    enemy_sprites_group = pygame.sprite.Group()

    # Create sprites to fill groups

    # Create enemy sprites
    for i in range(num_enemy):
        enemy = Enemy()
        player = Player()

        # Add the enemy sprites to enemy_sprites_group
        enemy_sprites_group.add(enemy)

        # Add the player sprites to enemy_sprites_group
        enemy_sprites_group.add(player)

    # ----- MAIN LOOP
    while not done:
        # -- Event Handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        # ----- LOGIC
        # Update enemy sprites
        enemy_sprites_group.update()

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
