from typing import Tuple, Union

import pygame.sprite

from constants import WIDTH, HEIGHT
from pong_protocol.protocol import Event


class Player(pygame.sprite.Sprite):
    LEFT = 1
    RIGHT = 2

    def __init__(self, up_key, down_key, stick_to):
        super(Player, self).__init__()
        self.window_height = HEIGHT
        self.window_width = WIDTH
        self.up_key = up_key
        self.down_key = down_key
        self.stick_to = stick_to
        self.orig_width, self.orig_height = int(WIDTH * 0.02), int(HEIGHT * 0.2)

        self.surf = pygame.Surface((self.orig_width, self.orig_height))
        self.surf.fill((255, 255, 255))

        center = self.get_center(stick_to)

        self.event_available = False
        self.rect = self.surf.get_rect(center=center)
        self.orig_offset_x = 0
        self.orig_offset_y = 0
        self.orig_offset_step = int(HEIGHT * 0.02)
        self.offset_step = self.orig_offset_step

    def get_center(self, stick_to, width=WIDTH, height=HEIGHT) -> Tuple[Union[int, float], Union[int, float]]:
        if stick_to == self.LEFT:
            return 0, height * 0.5
        elif stick_to == self.RIGHT:
            return width, height * 0.5

    def scale(self, window_width, window_height):
        self.window_width, self.window_height = window_width, window_height

        width = self.to_scaled_width(self.orig_width)
        height = self.to_scaled_height(self.orig_height)

        self.surf = pygame.transform.scale(self.surf, (width, height))
        self.surf.fill((255, 255, 255))
        center = self.get_center(stick_to=self.stick_to, width=window_width, height=window_height)
        self.rect = self.surf.get_rect(center=center)
        self.rect.move_ip((self.to_scaled_width(self.orig_offset_x), self.to_scaled_height(self.orig_offset_y)))

    def to_scaled_height(self, height):
        return int(height * self.window_height / HEIGHT)

    def to_scaled_width(self, width):
        return int(width * self.window_width / WIDTH)

    def move_to(self, remote_height):
        difference = self.orig_offset_y - remote_height
        self.orig_offset_y = remote_height
        self.rect.move_ip((0, -self.to_scaled_height(difference)))

    def proceed(self, key_pressed):
        if key_pressed[self.up_key] and self.rect.centery - self.rect.height / 2 > 0:
            self.event_available = True
            self.orig_offset_y -= self.orig_offset_step
            self.rect.move_ip((0, -self.to_scaled_height(self.orig_offset_step)))
        elif key_pressed[self.down_key] and self.rect.height / 2 + self.rect.centery < self.window_height:
            self.event_available = True
            self.orig_offset_y += self.orig_offset_step
            self.rect.move_ip((0, self.to_scaled_height(self.orig_offset_step)))

    def get_event(self):
        if self.event_available:
            self.event_available = False
            return Event(type='remote_height', remote_height=self.orig_offset_y)


def get_sprites():
    player1 = Player(pygame.K_w, pygame.K_s, stick_to=Player.LEFT)
    player2 = Player(pygame.K_UP, pygame.K_DOWN, stick_to=Player.RIGHT)
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player1)
    all_sprites.add(player2)
    return all_sprites, player2
