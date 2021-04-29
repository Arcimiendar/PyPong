import time
from typing import Tuple, Union

import pygame.sprite
import random

from constants import WIDTH, HEIGHT
from pong_protocol.event import Event

random.seed(time.time())


class ScaledMixin:
    def __init__(self):
        self.window_height = HEIGHT
        self.window_width = WIDTH

        super(ScaledMixin, self).__init__()

    def to_scaled_height(self, height):
        return int(height * self.window_height / HEIGHT)

    def to_scaled_width(self, width):
        return int(width * self.window_width / WIDTH)


class Player(ScaledMixin, pygame.sprite.Sprite):
    LEFT = 1
    RIGHT = 2

    def __init__(self, up_key, down_key, stick_to):
        super(Player, self).__init__()
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


class Ball(ScaledMixin, pygame.sprite.Sprite):
    def __init__(self, left_board: Player, right_board: Player):
        super(Ball, self).__init__()
        self.left_board, self.right_board = left_board, right_board

        self.orig_width = int(WIDTH * 0.01)
        self.orig_height = int(WIDTH * 0.01)
        self.surf = pygame.Surface((self.orig_width, self.orig_height))
        self.surf.fill((255, 255, 255))

        self.orig_speed = int(HEIGHT * 0.01)
        self.orig_offset_y = int(self.window_height / 2)
        self.orig_offset_x = int(self.window_width / 2)
        self.speed_vector = []
        self.speed_vector = [-1 if random.random() > 0.5 else 1, -1 if random.random() > 0.5 else 1]

        self.rect = self.surf.get_rect(center=(self.orig_offset_x, self.orig_offset_y))
        # def scale(self):

    def scale(self, window_width, window_height):
        self.window_width, self.window_height = window_width, window_height

        width = self.to_scaled_width(self.orig_width)
        height = self.to_scaled_width(self.orig_height)

        self.surf = pygame.transform.scale(self.surf, (width, height))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(
            center=(self.to_scaled_width(self.orig_offset_x), self.to_scaled_height(self.orig_offset_y))
        )
        # self.rect.move_ip((self.to_scaled_width(self.orig_offset_x), self.to_scaled_height(self.orig_offset_y)))

    def get_current_ball_coords_event(self) -> Event:
        return Event(type=Event.REMOTE_BALL_COORDS, remote_width=self.orig_offset_x, remote_height=self.orig_offset_y)

    def move_to(self, remote_width, remote_height):
        difference_y = self.orig_offset_y - remote_height
        difference_x = self.orig_offset_x - remote_width
        self.orig_offset_y = remote_height
        self.orig_offset_x = remote_width
        self.rect.move_ip((-self.to_scaled_width(difference_x), -self.to_scaled_height(difference_y)))

    def proceed(self):
        pos_x = self.orig_offset_x + self.speed_vector[0] * self.orig_speed
        pos_y = self.orig_offset_y + self.speed_vector[1] * self.orig_speed
        if pos_y + self.orig_height / 2 > HEIGHT or pos_y - self.orig_height / 2 < 0:
            self.speed_vector[1] *= -1

        elif pos_x + self.orig_width / 2 > WIDTH or pos_x - self.orig_width / 2 < 0:
            self.__init__(self.left_board, self.right_board)
            return

        elif pos_x + self.orig_width / 2 > WIDTH - self.right_board.orig_width / 2 and \
                self.right_board.orig_offset_y - self.right_board.orig_height / 2 + HEIGHT / 2 < \
                pos_y < self.right_board.orig_offset_y + self.right_board.orig_height / 2 + HEIGHT / 2 or \
                pos_x - self.orig_width / 2 < self.left_board.orig_width / 2 and \
                self.left_board.orig_offset_y - self.left_board.orig_height / 2 + HEIGHT / 2 < \
                pos_y < self.left_board.orig_offset_y + self.left_board.orig_height / 2 + HEIGHT / 2:

            self.speed_vector[0] *= -1

        self.move_to(pos_x, pos_y)


def get_sprites():
    player1 = Player(pygame.K_w, pygame.K_s, stick_to=Player.LEFT)
    player2 = Player(pygame.K_UP, pygame.K_DOWN, stick_to=Player.RIGHT)
    ball = Ball(player1, player2)
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player1)
    all_sprites.add(player2)
    all_sprites.add(ball)
    return all_sprites, player1, player2, ball
