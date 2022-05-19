# Pygame Project

import pygame
import random

# ----- CONSTANTS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
SKY_BLUE = (95, 165, 228)
WIDTH = 1280
HEIGHT = 720
ENEMY_VELOCITY = 5
PLAYER_VELOCITY = 10
TITLE = "Shinning Upon You"

# Create a background house
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
        self.rect.center = (WIDTH / 2, 0)

        # Sun velocity
        self.xvel = PLAYER_VELOCITY

        # Call the added parameter
        self.player = player

    def update(self):
        # Move with the player in the x direction
        if (self.rect.centerx -13) < self.player.rect.centerx:
            self.rect.x += self.xvel
        if (self.rect.centerx -13) > self.player.rect.centerx:
            self.rect.x -= self.xvel


# Create a player (rays) class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Image
        self.image = pygame.image.load("./assets/rays.png")
        self.image = pygame.transform.scale(self.image, (self.image.get_width() / 2, HEIGHT))

        # Rect
        self.rect = self.image.get_rect()

        # Start player velocity
        self.xvel = 0

        # Start player Location
        self.rect.top = 0
        self.rect.right = WIDTH / 2

    # Player Movements
        self.xvel = 0

    def move_left(self):
        self.xvel = -PLAYER_VELOCITY

    def move_right(self):
        self.xvel = PLAYER_VELOCITY

    def stop(self):
        self.xvel = 0

    # Update the player
    def update(self):
        # According to player movements
        self.rect.x += self.xvel

        # Prevent the player from going off the screen
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT


# Create enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, protect):
        super().__init__()

        # Image
        self.image = pygame.image.load("./assets/butterfly_enemy.png")
        self.image = pygame.transform.scale(self.image, (38, 38))

        # Rect
        self.rect = self.image.get_rect()

        # Location
        self.rect.center = random.choice([
            (random.randrange(-100, 0), random.randrange(0, HEIGHT)),
            (random.randrange(WIDTH, WIDTH + 100), random.randrange(0, HEIGHT))
        ])

        # Enemy velocity
        self.xvel = ENEMY_VELOCITY
        self.yvel = ENEMY_VELOCITY

        # Call the added parameter
        self.protect = protect

    def update(self):
        # Make the enemy move to the x direction randomly
        if random.random() >= 0.2:
            # Move closer to the protect in the x direction
            if self.rect.x < self.protect.rect.centerx:
                self.rect.x += self.xvel
            if self.rect.x > self.protect.rect.centerx:
                self.rect.x -= self.xvel
        else:
            # Move closer to the protect in the y direction
            if self.rect.y < self.protect.rect.centery:
                self.rect.y += self.yvel
            if self.rect.y > self.protect.rect.centery:
                self.rect.y -= self.yvel


# Create protect class
class Protect(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()

        # Images
        self.happy_image = pygame.image.load("./assets/happy_face.png")
        self.happy_image = pygame.transform.scale(
            self.happy_image,
            (self.happy_image.get_width() / 8, self.happy_image.get_height() / 8)
        )
        self.regular_image = pygame.image.load("./assets/normal_face.png")
        self.regular_image = pygame.transform.scale(
            self.regular_image,
            (self.regular_image.get_width() / 8, self.regular_image.get_height() / 8)
        )
        self.sad_image = pygame.image.load("./assets/sad_face.png")
        self.sad_image = pygame.transform.scale(
            self.sad_image,
            (self.sad_image.get_width() / 8, self.sad_image.get_height() / 8)
        )

        # Rendered image under normal situation
        self.image = self.regular_image

        # Rect
        self.rect = self.image.get_rect()

        # Location
        self.rect.center = (WIDTH / 2,  HEIGHT - self.image.get_height() + 65)

        # Call the added parameter
        self.player = player


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
    score = 0
    health = 10

    # Sounds
    hit_sound = pygame.mixer.Sound("./assets/hit_sound.ogg")
    hit_sound.set_volume(0.5)
    losing_sound = pygame.mixer.Sound("./assets/Losing_sound.ogg")
    losing_sound.set_volume(1)
    background_sound = pygame.mixer.Sound("./assets/background_music.ogg")
    background_sound.set_volume(1)
    attacked_sound = pygame.mixer.Sound("./assets/attacked_sound.ogg")
    attacked_sound.set_volume(0.5)

    # Play background sound
    background_sound.play()

    # Sprite groups
    all_sprites_group = pygame.sprite.Group()
    enemy_sprites_group = pygame.sprite.Group()
    protect_sprites_group = pygame.sprite.Group()

    # Add player to all_sprites_group
    player = Player()
    all_sprites_group.add(player)

    # Add protect to all_sprites_group and protect_sprites_group
    protect = Protect(player)
    all_sprites_group.add(protect)
    protect_sprites_group.add(protect)

    # Add sun to all_sprites_group
    sun = Sun(player)
    all_sprites_group.add(sun)

    # Create enemy sprite group
    for i in range(num_enemy):
        enemy = Enemy(protect)

        # Add enemy to both list: all_sprites_group and enemy_sprites_group
        all_sprites_group.add(enemy)
        enemy_sprites_group.add(enemy)

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

        # ----- LOGIC
        # Update all sprites group
        all_sprites_group.update()

        # Collision between player and enemy sprites
        collided_enemy = pygame.sprite.spritecollide(
            player,
            enemy_sprites_group,
            dokill=True
        )

        # Collision between protect and enemy sprites
        attacked_enemy = pygame.sprite.spritecollide(
            protect,
            enemy_sprites_group,
            dokill=True
        )

        # Collision between player and protect sprites
        happy_protect = pygame.sprite.spritecollide(
            player,
            protect_sprites_group,
            dokill=False
        )

        # Create a happy protect face when protect collided with player
        # Create a sad face when health goes below 5
        if health <= 5:
            protect.image = protect.sad_image
        elif happy_protect:
            protect.image = protect.happy_image
        else:
            protect.image = protect.regular_image

        # Iterate through all collided enemy with player and replace with new enemies
        for enemy in collided_enemy:
            enemy = Enemy(protect)
            all_sprites_group.add(enemy)
            enemy_sprites_group.add(enemy)

        # Iterate through all collided enemy with protect and replace with new enemies
        for enemy in attacked_enemy:
            enemy = Enemy(protect)
            all_sprites_group.add(enemy)
            enemy_sprites_group.add(enemy)

        # Add one to score if player and enemy collided
        if len(collided_enemy) > 0:
            score += 1

            # Play sound when the player and enemy collide
            attacked_sound.play()

        # Remove one to health if protect and enemy collided
        if len(attacked_enemy) > 0:
            health -= 1

            # Play sound when the enemy and protect collide and a different sound if health goes below 5
            if health >= 5:
                hit_sound.play()
            else:
                losing_sound.play()

        # ----- RENDER
        screen.fill(BLACK)
        screen.blit(background_image,
                    ((WIDTH - background_image.get_width()) / 2, (HEIGHT - background_image.get_height()) + 10))

        # Draw all sprites in the screen
        all_sprites_group.draw(screen)

        # Render score
        default_font = pygame.font.SysFont("SERIF", 20)
        score_surf = default_font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_surf, (10, 10))

        # Render health
        health_sirf = default_font.render(f"Health: {health}", True, WHITE)
        screen.blit(health_sirf, (200, 10))

        # Render lose screen
        if health <= 0:
            ending_credit = default_font.render("You have failed to protect the life of Mr.Cat. "
                                                f"You score is: {score}. Please try again in your next life. Goodbye!",
                                                True,
                                                WHITE)
            screen.blit(ending_credit, (225, HEIGHT // 2))
            pygame.display.flip()
            pygame.mixer.fadeout(5000)
            pygame.time.wait(5000)
            done = True

        # Render Win screen
        if score == 100:
            winning_credit = default_font.render("You have successfully protect Mr.Cat."
                                                 f" You score is: {score}."
                                                 " Mr.Cat welcomes your visit again anytime. Goodbye!",
                                           True,
                                           WHITE)
            screen.blit(winning_credit, (225, HEIGHT // 2))
            pygame.display.flip()
            pygame.mixer.fadeout(5000)
            pygame.time.wait(5000)
            done = True

        # ----- UPDATE DISPLAY
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
