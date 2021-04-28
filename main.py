import pygame

from constants import WIDTH, HEIGHT, FPS
from sprites import get_sprites

# ACC = 0.5
# FRIC = -0.12

# def game_logic()


def main():
    height = HEIGHT
    width = WIDTH

    pygame.init()

    frame_per_sec = pygame.time.Clock()

    display_surface = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    pygame.display.set_caption("PyPong")
    sprites = get_sprites()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                width = event.w
                height = event.h
                for entity in sprites:
                    entity.scale(width, height)

        key_pressed = pygame.key.get_pressed()

        display_surface.fill((0, 0, 0))
        for entity in sprites:
            entity.proceed(key_pressed)
            display_surface.blit(entity.surf, entity.rect)

        pygame.display.update()
        frame_per_sec.tick(FPS)

    pygame.quit()


if __name__ == '__main__':
    main()
