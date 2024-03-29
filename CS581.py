import math
import random
import sys

import pygame
from pygame import mixer

# Intialize the pygame
pygame.init()

# create the screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Background
background = pygame.image.load(r"C:\Users\divya\OneDrive\Desktop\Spring 2023\CS581\background.png").convert()

# Sound
mixer.music.load(r"C:\Users\divya\OneDrive\Desktop\Spring 2023\CS581\background.wav")
mixer.music.play(-1)

# Caption and Icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load(r"C:\Users\divya\OneDrive\Desktop\Spring 2023\CS581\ufo.png").convert()
pygame.display.set_icon(icon)


# Player
playerImg = pygame.image.load(r"C:\Users\divya\OneDrive\Desktop\Spring 2023\CS581\player.png").convert()
a=30
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
ENEMY_SPEED = 4
num_of_enemies = 6
enemy_speed = ENEMY_SPEED

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load(r"C:\Users\divya\OneDrive\Desktop\Spring 2023\CS581\enemy.png")).convert()
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))


# Bullet

# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving

bulletImg = pygame.image.load(r"C:\Users\divya\OneDrive\Desktop\Spring 2023\CS581\bullet.png").convert()
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# Score

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
testY = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render(f"Score: {score_value}", True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def isCollision(enemyX, enemyY, bulletX, bulletY):
    if distance(enemyX, enemyY, bulletX, bulletY) < 27:
        return True
    else:
        return False

# Define a dictionary mapping keys to movements
key_to_movement = {
    pygame.K_LEFT: -5,
    pygame.K_RIGHT: 5
}

# Game Loop
running = True
while running:

    # RGB = Red, Green, Blue
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key in key_to_movement:
                playerX_change = key_to_movement[event.key]
            if event.key == pygame.K_SPACE and bullet_state == "ready":
                bulletSound = mixer.Sound(r"C:\Users\divya\OneDrive\Desktop\Spring 2023\CS581\laser.wav")
                bulletSound.play()
                # Get the current x cordinate of the spaceship
                bulletX = playerX
                fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key in key_to_movement:
                playerX_change = 0

    # 5 = 5 + -0.1 -> 5 = 5 - 0.1
    # 5 = 5 + 0.1

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy Movement

    for i, (enemy_x, enemy_y) in enumerate(zip(enemyX, enemyY)):
    # Game Over
        if enemy_y > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemy_speed
        if enemyX[i] <= 0:
            enemy_speed = ENEMY_SPEED
            enemyY[i] += 40
        elif enemyX[i] >= SCREEN_WIDTH - 64:
            enemy_speed = -ENEMY_SPEED
            enemyY[i] += 40

        # Collision
        collision = isCollision(enemy_x, enemy_y, bulletX, bulletY)
        if collision:
            explosionSound = mixer.Sound(r"C:\Users\divya\OneDrive\Desktop\Spring 2023\CS581\explosion.wav")
            explosionSound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    else:
        bulletY -= bulletY_change
        fire_bullet(bulletX, bulletY)

    player(playerX, playerY)
    show_score(textX, testY)
    pygame.display.update()