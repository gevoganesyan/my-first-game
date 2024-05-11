import asyncio
import sys

import pygame


FPS = 25
SCREEN_SIZE = (1200, 800)


async def main():
    pygame.init()
    screen: pygame.Surface = pygame.display.set_mode(SCREEN_SIZE)
    clock = pygame.time.Clock()

    screen.fill('aquamarine')  # https://www.pygame.org/docs/ref/color_list.html
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if not event.type == pygame.KEYUP:
                continue

            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

        clock.tick(FPS)
        await asyncio.sleep(0)


if __name__ == '__main__':
    asyncio.run(main())
