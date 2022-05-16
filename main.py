# Pygame Project

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
ENEMY_VELOCITY = 0
TITLE = "Shinning Over You"

# Create a background
background_image = pygame.image.load("./assets/house.png")
background_image = pygame.transform.scale(background_image, (533 / 2, 468 / 2))

# Create a sun class
class Sun(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()

        # Image
        self.image = pygame.image.load("./assets/sun.png")

        # Rect
        self.rect = self.image.get_rect()

        # Location
        self.rect.center = (0, WIDTH // 2)

        # Sun velocity
        self.xvel = 10

        self.player = player

    def update(self):
        # Move with the player in the x direction
        if self.rect.x < self.player.rect.centerx:
            self.rect.x += self.xvel
        if self.rect.x > self.player.rect.centerx:
            self.rect.x -= self.xvel

# Create a player (rays) class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Image
        self.image = pygame.image.load("./assets/rays.png")
        self.image = pygame.transform.scale(self.image, (self.image.get_width(), HEIGHT))

        # Rect
        self.rect = self.image.get_rect()

        # Starting player velocity
        self.xvel = 0

        # Starting player Location
        self.rect.top = 0
        self.rect.right = WIDTH // 2

    # Player Movements
        self.xvel = 0

    def move_left(self):
        self.xvel = -10

    def move_right(self):
        self.xvel = 10

    def stop(self):
        self.xvel = 0

    # Update the player
    def update(self):
        # According to player movements
        self.rect.x += self.xvel


# Create enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, protect):
        super().__init__()

        # Image
        self.image = pygame.image.load("./assets/butterfly_enemy.png")
        self.image = pygame.transform.scale(self.image, (38, 38))
        self.image.set_colorkey(WHITE)

        # Rect
        self.rect = self.image.get_rect()

        # Location
        self.rect.center = random_coords()

        # Enemy velocity
        self.xvel = 2
        self.yvel = 2

        self.protect = protect

    def update(self):
        # Move closer to the protect in the x direction
        if self.rect.x < self.protect.rect.centerx:
            self.rect.x += self.xvel
        if self.rect.x > self.protect.rect.centerx:
            self.rect.x -= self.xvel

        # Move closer to the protect in the y direction
        if self.rect.y < self.protect.rect.centery:
            self.rect.y += self.yvel
        if self.rect.y > self.protect.rect.centery:
            self.rect.y -= self.yvel


def random_coords() -> list:
    """Returns a random x, y coordinate between
    0 to WIDTH and 0 to HEIGHT respectively"""
    return random.randrange(0, WIDTH), random.randrange(0, HEIGHT)

# Create protect class
class Protect(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Image
        self.image = pygame.image.load("./assets/normal_face.png")
        self.image = pygame.transform.scale(self.image,
                                            (self.image.get_width() / 8,
                                             self.image.get_height() / 8))

        # Rect
        self.rect = self.image.get_rect()

        # Location
        self.rect.center = (WIDTH / 2,  HEIGHT - self.image.get_height() + 65)


def main():
    pygame.init()

    # ----- SCREEN PROPERTIES
    size = (WIDTH, HEIGHT)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption(TITLE)

    # ----- LOCAL VARIABLES
    done = False
    clock = pygame.time.Clock()
    num_enemy = 20

    # Sprite groups
    all_sprites_group = pygame.sprite.Group()
    enemy_sprites_group = pygame.sprite.Group()

    # Add protect to all_sprites_group
    protect = Protect()
    all_sprites_group.add(protect)

    # Create enemy sprite group
    for i in range(num_enemy):
        enemy = Enemy(protect)

        # Add enemy to both list: all_sprites_group and enemy_sprites_group
        all_sprites_group.add(enemy)
        enemy_sprites_group.add(enemy)

    # Add player to all_sprites_group
    player = Player()
    all_sprites_group.add(player)

    # Add sun to all_sprites_group
    sun = Sun()
    all_sprites_group.add(sun)

    score = 0

    # ----- MAIN LOOP
    while not done:
        # -- Event Handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            # Move player according to pressed key
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    player.move_right()
                if event.key == pygame.K_LEFT:
                    player.move_left()

            # Stop player if no key is pressed
            if event.type == pygame.KEYUP:
                player.stop()

            # Set boundaries for the player
            if player.rect.right > WIDTH:
                player.rect.right = WIDTH
            if player.rect.left < 0:
                player.rect.left = 0

        # ----- LOGIC

        all_sprites_group.update()

        # Collision between player and enemy sprites
        collided_enemy = pygame.sprite.spritecollide(
            player,
            enemy_sprites_group,
            dokill = True
        )

        # Collision between protect and enemy sprites
        attacked_enemy = pygame.sprite.spritecollide(
            protect,
            enemy_sprites_group,
            dokill = True
        )

        # Add one to score if player and enemy collided
        if len(collided_enemy) > 0:
            score += 1

        # Remove one to health if protect and enemy collided
        health = 3
        if len(attacked_enemy) > 0:
            health -= 1

        # ----- RENDER
        screen.fill(BLACK)
        screen.blit(background_image,
                    ((WIDTH - background_image.get_width()) / 2, (HEIGHT - background_image.get_height()) + 10))

        # Add house to the background
        all_sprites_group.draw(screen)

        # Render score
        default_font = pygame.font.SysFont("SERIF", 20)
        score_surf = default_font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_surf, (10, 10))

        # Render health
        health_sirf = default_font.render(f"Health: {health}", True, WHITE)
        screen.blit(health_sirf, (100, 10))

        # ----- UPDATE DISPLAY
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
