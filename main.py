import pygame

from itertools import chain
from constants import WIDTH, HEIGHT, FPS
from sprites import get_sprites
from pong_protocol.protocol import PongProtocol

already_here = False


def main(pong_protocol: PongProtocol):
    global already_here
    if already_here:
        return
    already_here = True
    height = HEIGHT
    width = WIDTH

    pygame.init()

    frame_per_sec = pygame.time.Clock()

    display_surface = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    pygame.display.set_caption("PyPong")
    sprites, this_board, enemy_board = get_sprites()

    running = True
    while running:
        for event in chain(pygame.event.get(), pong_protocol.get_available_events()):
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                width = event.w
                height = event.h
                for entity in sprites:
                    entity.scale(width, height)
            elif event.type == 'remote_height':
                enemy_board.move_to(event.remote_height)

        key_pressed = pygame.key.get_pressed()
        this_board.proceed(key_pressed)

        display_surface.fill((0, 0, 0))
        for entity in sprites:
            # entity.proceed(key_pressed)
            display_surface.blit(entity.surf, entity.rect)


        event = this_board.get_event()
        if event:
            pong_protocol.sendLine(event.to_line())

        pygame.display.update()
        frame_per_sec.tick(FPS)

    pygame.quit()
