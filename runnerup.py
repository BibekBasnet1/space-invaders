# pygame demonstration
import pygame
import random
import math

# initializing width and height for the screem
width = 1000
height = 800
pygame.init()
clock = pygame.time.Clock()
# for screen
screen = pygame.display.set_mode((width, height))

# background music
pygame.mixer.music.load('invadersBackground.mp3')
pygame.mixer.music.play(-1)

# set caption
pygame.display.set_caption("Space invaders - By Bibek Basnet ")
icon = pygame.image.load("uranus.png")
pygame.display.set_icon(icon)

# player
playerImg = pygame.image.load("spaceship1.png")
playerX = 480
playerY = 650
playerX_Change = 0

# enemy
enemyImg = []
enemy_playerX = []
enemy_playerY = []
enemyX_change = []
enemyY_change = []
number_of_enemies = 5
# for creating the number_of_enemies
for i in range(number_of_enemies):
    enemyImg.append(pygame.image.load("spaceship2.png"))
    enemy_playerX.append(random.randint(0, 936))
    enemy_playerY.append(random.randint(50, 500))
    enemyX_change.append(0.3)
    enemyY_change.append(10)

# bullet
bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 650
bulletX_Change = 0
bulletY_change = 1.5
bullet_position = "ready"

# score
score_value = 0
font = pygame.font.SysFont('Helvetica', 32)
textX = 10
textY = 10

# game over text
game_over_font = pygame.font.SysFont('Arial', 70)


def show_score(x, y):
    score = font.render("score : " + str(score_value), True, (200, 150, 35))
    screen.blit(score, (x, y))


def fire_bullet(x, y):
    global bullet_position
    bullet_position = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def game_over_text():
    over_text = game_over_font.render("GAME OVER", True, (34, 243, 200))
    screen.blit(over_text, (300, 300))


# background
background = pygame.image.load("bb.jpg")


def player(x, y):
    # to draw the image on the surface NOte: surface means screen
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    # to draw the image on the surface NOte: surface means screen
    screen.blit(enemyImg[i], (x, y))


def isCollision(bulletx, bullety, enemyx, enemyy):
    distance = math.sqrt((math.pow(enemyx - bulletx, 2)) + (math.pow(enemyy - bullety, 2)))
    if distance < 27:
        return True


sound = True


def game_over_sound():
    global sound
    # sound = True
    if sound:
        over = pygame.mixer.Sound('gameover.wav')
        over.play()
        sound = False


# setting an infinite loop to actually keep the screen until we decide to close by ourselves
run = True
while run:
    # for every event that occurs
    screen.fill((205, 133, 63))
    screen.blit(background, (0, 0))
    # screen.blit(bulletImg, (playerX bulletY - 10))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        # if keystroke are pressed check whether it is right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                # print("left key pressed")
                playerX_Change -= 0.7
            if event.key == pygame.K_RIGHT:
                # print("Right key is pressed")
                playerX_Change += 0.7

            if event.key == pygame.K_SPACE:
                # this makes the bullet go upwards
                if bullet_position == "ready":
                    bullet_sound = pygame.mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_Change = 0
                # print("Keystroke has been released")
    # to fill out the screen with color and updating the screen so that we can actually see it
    playerX += playerX_Change  # this changes the value after we key press based on left or right

    if playerX <= 0:
        playerX = 0
    elif playerX >= 936:
        playerX = 936

    for i in range(number_of_enemies):
        # game over
        if enemy_playerY[i] > 590:
            for j in range(number_of_enemies):
                enemy_playerY[j] = 2000
            game_over_sound()
            game_over_text()
            break
        enemy_playerX[i] += enemyX_change[i]
        if enemy_playerX[i] <= 0:
            enemyX_change[i] = 0.5
            enemy_playerY[i] += enemyY_change[i]
        elif enemy_playerX[i] >= 936:
            enemyX_change[i] = -0.5
            enemy_playerY[i] += enemyY_change[i]

        # for collision
        collision = isCollision(enemy_playerX[i], enemy_playerY[i], bulletX, bulletY)
        if collision:
            collision_sound = pygame.mixer.Sound('laser.wav')
            collision_sound.play()
            bulletY = 650
            bullet_position = "ready"
            score_value += 1
            enemy_playerX[i] = random.randint(0, 936)
            enemy_playerY[i] = random.randint(5, 500)

        enemy(enemy_playerX[i], enemy_playerY[i], i)

    # for moving the bullet
    if bulletY <= 0:
        bulletY = 650
        bullet_position = "ready"

    if bullet_position == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    show_score(textX, textY)
    player(playerX, playerY)
    pygame.display.update()
