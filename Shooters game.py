import time

import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Simple Shooter Game")

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# Clock and frame rate
clock = pygame.time.Clock()
fps = 60

# Load assets
player_img = pygame.image.load("player.png")  # Spaceship image
enemy_img = pygame.image.load("enemy.png")  # Enemy image
bullet_img = pygame.image.load("bullet.png")  # Bullet image

# Scale images
player_img = pygame.transform.scale(player_img, (50, 50))
enemy_img = pygame.transform.scale(enemy_img, (40, 40))
bullet_img = pygame.transform.scale(bullet_img, (10, 20))

# Background
background = pygame.image.load("background.jpg")
background = pygame.transform.scale(background, (width, height))

# Player class
class Player:
    def __init__(self):
        self.x = width // 2
        self.y = height - 70
        self.speed = 5
        self.width = 50
        self.height = 50

    def draw(self):
        screen.blit(player_img, (self.x, self.y))

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < width - self.width:
            self.x += self.speed

# Bullet class
class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = -7

    def draw(self):
        screen.blit(bullet_img, (self.x, self.y))

    def move(self):
        self.y += self.speed

# Enemy class
class Enemy:
    def __init__(self):
        self.x = random.randint(0, width - 40)
        self.y = random.randint(-100, -40)
        self.speed = random.randint(2, 5)

    def draw(self):
        screen.blit(enemy_img, (self.x, self.y))

    def move(self):
        self.y += self.speed
        if self.y > height:
            self.x = random.randint(0, width - 40)
            self.y = random.randint(-100, -40)

# Main game loop
def game_loop():
    player = Player()
    bullets = []
    enemies = [Enemy() for _ in range(5)]  # 5 enemies
    score = 0
    running = True

    font = pygame.font.SysFont("comicsans", 30)

    while running:
        screen.blit(background, (0, 0))  # Draw background
        player.draw()

        # Display score
        score_text = font.render(f"Score: {score}", True, white)
        screen.blit(score_text, (10, 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Shoot bullet
                    bullets.append(Bullet(player.x + player.width // 2 - 5, player.y))

        # Move and draw bullets
        for bullet in bullets[:]:
            bullet.move()
            bullet.draw()
            # Remove bullets that go off-screen
            if bullet.y < -20:
                bullets.remove(bullet)

        # Move and draw enemies
        for enemy in enemies:
            enemy.move()
            enemy.draw()

            # Check collision with bullets
            for bullet in bullets[:]:
                if enemy.x < bullet.x < enemy.x + 40 and enemy.y < bullet.y < enemy.y + 40:
                    enemies.remove(enemy)
                    bullets.remove(bullet)
                    score += 1
                    enemies.append(Enemy())

            # Check collision with player
            if enemy.x < player.x < enemy.x + 40 and enemy.y < player.y < enemy.y + 40:
                running = False  # Game over

        # Move player
        keys = pygame.key.get_pressed()
        player.move(keys)

        pygame.display.update()
        clock.tick(fps)

    # Game Over screen
    screen.fill(black)
    game_over_text = font.render("GAME OVER", True, red)
    score_text = font.render(f"Final Score: {score}", True, white)
    screen.blit(game_over_text, (width // 2 - 100, height // 2 - 50))
    screen.blit(score_text, (width // 2 - 100, height // 2))
    pygame.display.update()
    time.sleep(3)

# Run the game
game_loop()
pygame.quit()
