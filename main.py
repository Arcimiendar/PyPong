import pygame
import sys

from twisted.internet import reactor
from typing import TYPE_CHECKING
from itertools import chain
from constants import WIDTH, HEIGHT, FPS
from sprites import get_sprites
from pong_protocol.event import Event


if TYPE_CHECKING:
    from pong_protocol.protocol import PongProtocol


def main(pong_protocol: 'PongProtocol'):

    is_server = pong_protocol.is_server
    height = HEIGHT
    width = WIDTH

    pygame.init()

    frame_per_sec = pygame.time.Clock()

    display_surface = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    pygame.display.set_caption("PyPong")
    sprites, this_board, enemy_board, ball = get_sprites()

    running = True
    while running:
        for event in chain(pygame.event.get(), pong_protocol.get_available_events()):
            if event.type == pygame.QUIT:
                running = False
                pong_protocol.sendLine(Event(type=Event.QUIT).to_line())
            elif event.type == pygame.VIDEORESIZE:
                width = event.w
                height = event.h
                for entity in sprites:
                    entity.scale(width, height)
            elif event.type == Event.REMOTE_HEIGHT:
                enemy_board.move_to(event.remote_height)
            elif event.type == Event.QUIT:
                running = False
            elif event.type == Event.REMOTE_BALL_COORDS and not is_server:
                ball.move_to(event.remote_width, event.remote_height)

        key_pressed = pygame.key.get_pressed()
        this_board.proceed(key_pressed)

        event = this_board.get_event()
        if event:
            pong_protocol.sendLine(event.to_line())

        event = ball.get_current_ball_coords_event()
        pong_protocol.sendLine(event.to_line())

        if is_server:
            ball.proceed()

        display_surface.fill((0, 0, 0))
        for entity in sprites:
            display_surface.blit(entity.surf, entity.rect)

        pygame.display.update()
        frame_per_sec.tick(FPS)

    pygame.quit()
    reactor.callFromThread(reactor.stop)
