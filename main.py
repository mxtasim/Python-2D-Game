# The Battle 2D game

import pygame
import os

pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("THE BATTLE")  # Game title

WHITE = (255, 255, 255)  # Color 1
BLACK = (0, 0, 0)  # Color 2
RED = (255, 0, 0)  # Color 3
YELLOW = (255, 255, 0)  # Color 4

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)  # Application window size

BULLET_HIT_SOUND = pygame.mixer.Sound('Assets/Grenade+1.mp3')  # Sound 1
BULLET_FIRE_SOUND = pygame.mixer.Sound('Assets/Gun+Silencer.mp3')  # Sound 2
BACKGROUND_MUSIC = pygame.mixer.Sound('Assets/BACKGROUND_MUSIC.mp3')  # Sound 3

HEALTH_FONT = pygame.font.SysFont('comicsans', 40) # Font 1
WINNER_FONT = pygame.font.SysFont('comicsans', 100)  # Font 2

FPS = 60 # Lock the fps
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 3
SOLDIER_WIDTH, SOLDIER_HEIGHT = 70, 70  

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

FIRST_SOLDIER_IMAGE = pygame.image.load(  # First soldier picture
    os.path.join('Assets', 'SOLDIER_1.png'))
FIRST_SOLDIER = pygame.transform.rotate(pygame.transform.scale(
    FIRST_SOLDIER_IMAGE, (SOLDIER_WIDTH, SOLDIER_HEIGHT)), 90)

SECOND_SOLDIER_IMAGE = pygame.image.load(  # Second soldier picture
    os.path.join('Assets', 'SOLDIER_2.png'))
SECOND_SOLDIER = pygame.transform.rotate(pygame.transform.scale(
    SECOND_SOLDIER_IMAGE, (SOLDIER_WIDTH, SOLDIER_HEIGHT)), 270)

BACKGROUND = pygame.transform.scale(pygame.image.load(  # Background picture
    os.path.join('Assets', 'BACKGROUND.png')), (WIDTH, HEIGHT))


def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.blit(BACKGROUND, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    red_health_text = HEALTH_FONT.render(
        "Health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render(
        "Health: " + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    WIN.blit(FIRST_SOLDIER, (yellow.x, yellow.y))
    WIN.blit(SECOND_SOLDIER, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()


def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:  # LEFT
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x:  # RIGHT
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:  # UP
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 15:  # DOWN
        yellow.y += VEL


def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:  # LEFT
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH:  # RIGHT
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0:  # UP
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 15:  # DOWN
        red.y += VEL


def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() /
                         2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)


def main():
    red = pygame.Rect(700, 300, SOLDIER_WIDTH, SOLDIER_HEIGHT)
    yellow = pygame.Rect(100, 300, SOLDIER_WIDTH, SOLDIER_HEIGHT)

    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

            BACKGROUND_MUSIC.play()  # BackGround Music
            
 
        winner_text = ""
        if red_health <= 0:
            winner_text = "PLAYER 1 WINS!"

        if yellow_health <= 0:
            winner_text = "PLAYER 2 WINS!"

        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(red, yellow, red_bullets, yellow_bullets,
                    red_health, yellow_health)

    main()


if __name__ == "__main__":
    main()
