import asyncio
import sys
from pathlib import Path

import pygame

# pygame.init()
pygame.font.init()
pygame.mixer.init()

CURRENT_FOLDER = Path(__file__).parent
ROOT_FOLDER = CURRENT_FOLDER.parent

SCREEN_SIZE = (1280, 720)  # (WIDTH, HEIGHT)
WINDOW = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption('First Game')

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

FPS = 60

BULLETS_SPEED = 7
MAX_BULLETS = 3

BORDER = pygame.Rect(SCREEN_SIZE[0] / 2 - 5, 0, 10, SCREEN_SIZE[1])

BULLET_HIT_SOUNDS = pygame.mixer.Sound(ROOT_FOLDER / CURRENT_FOLDER / 'Assets/Assets_Grenade+1.mp3')
BULLET_FIRE_SOUND = pygame.mixer.Sound(ROOT_FOLDER / CURRENT_FOLDER / 'Assets/Gun+Silencer.mp3')

HEALTH_FONT = pygame.font.SysFont('comics', 40)
WINNER_FONT = pygame.font.SysFont('comics', 100)

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2


YELLOW_SPACESHIP_IMAGE = pygame.image.load(ROOT_FOLDER / CURRENT_FOLDER / 'Assets' / 'spaceship_yellow.png')
YELLOW_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)


RED_SPACESHIP_IMAGE = pygame.image.load(ROOT_FOLDER / CURRENT_FOLDER / 'Assets' / 'spaceship_red.png')
RED_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

SPACE = pygame.transform.scale(pygame.image.load(CURRENT_FOLDER / 'Assets' / 'space.png'), SCREEN_SIZE)


def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WINDOW.blit(SPACE, (0, 0))
    pygame.draw.rect(WINDOW, BLACK, BORDER)

    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)
    WINDOW.blit(red_health_text, (SCREEN_SIZE[0] - red_health_text.get_width() - 10, 10))
    WINDOW.blit(yellow_health_text, (10, 10))

    WINDOW.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WINDOW.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WINDOW, RED, bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(WINDOW, YELLOW, bullet)
    pygame.display.update()


def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - 5 > 0:  # LEFT
        yellow.x -= 5
    if keys_pressed[pygame.K_d] and yellow.x + yellow.width < BORDER.x:  # RIGHT
        yellow.x += 5
    if keys_pressed[pygame.K_w] and yellow.y - 5 > 0:  # UP
        yellow.y -= 5
    if keys_pressed[pygame.K_s] and yellow.y + 5 + yellow.height < SCREEN_SIZE[1] - 10:  # DOWN
        yellow.y += 5


def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - 5 > BORDER.x + 15:  # LEFT
        red.x -= 5
    if keys_pressed[pygame.K_RIGHT] and red.x + 5 + red.width < SCREEN_SIZE[0] + 10:  # RIGHT
        red.x += 5
    if keys_pressed[pygame.K_UP] and red.y - 5 > 0:  # UP
        red.y -= 5
    if keys_pressed[pygame.K_DOWN] and red.y + 5 + red.height < SCREEN_SIZE[1] - 10:  # DOWN
        red.y += 5


def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLETS_SPEED
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > SCREEN_SIZE[0]:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLETS_SPEED
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WINDOW.blit(draw_text, (SCREEN_SIZE[0] / 2 - draw_text.get_width()/2,
                            SCREEN_SIZE[1]/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)


async def main():
    pygame.init()

    red = pygame.Rect(960, 360, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(320, 360, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

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
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height // 2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height // 2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUNDS.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUNDS.play()

        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow Wins!"
        if yellow_health <= 0:
            winner_text = "Red Wins!"
        if winner_text:
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)

        await asyncio.sleep(0)

    await main()


if __name__ == '__main__':
    asyncio.run(main())
