import time
from typing import Tuple, Union

import pygame.sprite
import random
import math

from constants import WIDTH, HEIGHT
from pong_protocol.event import Event

random.seed(time.time())


class ScaledMixin:
    def __init__(self, *args, **kwargs):
        self.window_height = HEIGHT
        self.window_width = WIDTH

        super(ScaledMixin, self).__init__(*args, **kwargs)

    def to_scaled_height(self, height):
        return height / HEIGHT * self.window_height

    def to_scaled_width(self, width):
        return width / WIDTH * self.window_width


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
        self.orig_offset_step = int(HEIGHT * 0.01)
        self.offset_step = self.orig_offset_step

    def get_center(self, stick_to) -> Tuple[Union[int, float], Union[int, float]]:
        if stick_to == self.LEFT:
            return self.to_scaled_width(0), self.to_scaled_height(HEIGHT * 0.5)
        elif stick_to == self.RIGHT:
            return self.to_scaled_width(WIDTH), self.to_scaled_height(HEIGHT * 0.5)

    def scale(self, window_width, window_height):
        self.window_width, self.window_height = window_width, window_height

        width = self.to_scaled_width(self.orig_width)
        height = self.to_scaled_height(self.orig_height)

        self.surf = pygame.transform.scale(self.surf, (int(width), int(height)))
        self.surf.fill((255, 255, 255))
        center = self.get_center(stick_to=self.stick_to)
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
    def __init__(self, left_board: Player, right_board: Player, keep_old_score=False):
        super(Ball, self).__init__()
        self.left_board, self.right_board = left_board, right_board
        if not keep_old_score:
            self.left_board_score = 0
            self.right_board_score = 0

        self.speed = 1.
        self.score_has_changed = True
        self.orig_width = int(WIDTH * 0.01)
        self.orig_height = int(WIDTH * 0.01)
        self.surf = pygame.Surface((self.orig_width, self.orig_height))
        self.surf.fill((255, 255, 255))

        self.orig_speed = int(HEIGHT * 0.002)
        self.orig_offset_y = int(self.window_height / 2)
        self.orig_offset_x = int(self.window_width / 2)
        self.speed_vector = []
        self.speed_vector = [-1 if random.random() > 0.5 else 1, -1 if random.random() > 0.5 else 1]

        self.rect = self.surf.get_rect(center=(self.orig_offset_x, self.orig_offset_y))

    def scale(self, window_width, window_height):
        self.window_width, self.window_height = window_width, window_height

        width = self.to_scaled_width(self.orig_width)
        height = self.to_scaled_width(self.orig_height)

        self.surf = pygame.transform.scale(self.surf, (int(width), int(height)))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(
            center=(self.to_scaled_width(self.orig_offset_x), self.to_scaled_height(self.orig_offset_y))
        )
        # self.rect.move_ip((self.to_scaled_width(self.orig_offset_x), self.to_scaled_height(self.orig_offset_y)))

    def get_current_ball_coords_event(self) -> Event:
        return Event(type=Event.REMOTE_BALL_COORDS, remote_width=self.orig_offset_x, remote_height=self.orig_offset_y)

    def move_to(self, remote_width, remote_height):
        difference_y = remote_height - self.orig_offset_y
        difference_x = remote_width - self.orig_offset_x
        self.orig_offset_y = remote_height
        self.orig_offset_x = remote_width
        self.rect.move_ip((self.to_scaled_width(difference_x), self.to_scaled_height(difference_y)))

    def proceed(self):
        diff_x = self.speed * self.speed_vector[0] * self.orig_speed
        diff_y = self.speed * self.speed_vector[1] * self.orig_speed

        diff_y = math.floor(diff_y) if diff_y < 0 else math.ceil(diff_y)
        diff_x = math.floor(diff_x) if diff_x < 0 else math.ceil(diff_x)

        pos_x = self.orig_offset_x + diff_x
        pos_y = self.orig_offset_y + diff_y

        if pos_y > HEIGHT:
            self.speed_vector[1] *= -1
            diff = pos_y - HEIGHT + self.orig_height / 2
            pos_y -= diff

        if pos_y < 0:
            self.speed_vector[1] *= -1
            diff = pos_y - self.orig_height / 2
            pos_y -= diff

        if pos_x >= WIDTH - self.right_board.orig_width / 2 and \
                self.right_board.orig_offset_y + (HEIGHT - self.right_board.orig_height) / 2 < \
                pos_y < \
                self.right_board.orig_offset_y + (HEIGHT + self.right_board.orig_height) / 2 \
                or pos_x <= self.left_board.orig_width / 2 and \
                self.left_board.orig_offset_y + (HEIGHT - self.left_board.orig_height) / 2 < \
                pos_y < \
                self.left_board.orig_offset_y + (HEIGHT + self.right_board.orig_height) / 2:

            self.speed_vector[0] *= -1
            self.speed *= 1.1

        elif pos_x + self.orig_width / 2 >= WIDTH or pos_x - self.orig_width / 2 <= 0:
            if pos_x + self.orig_width / 2 >= WIDTH:
                self.left_board_score += 1
                self.score_has_changed = True
            else:
                self.right_board_score += 1
                self.score_has_changed = True

            window_width, window_height = self.window_width, self.window_height
            self.__init__(self.left_board, self.right_board, keep_old_score=True)
            self.scale(window_width, window_height)
            return

        self.move_to(pos_x, pos_y)

    def get_score(self):
        return f'{self.left_board_score}-{self.right_board_score}'

    def get_score_event(self):
        self.score_has_changed = False
        return Event(type=Event.SCORE_UPDATE, score=self.get_score())


class Font(ScaledMixin, pygame.font.Font):
    def __init__(self, *args, **kwargs):
        super(Font, self).__init__(*args, **kwargs)
        self.orig_height = 64

def get_sprites():
    player1 = Player(pygame.K_w, pygame.K_s, stick_to=Player.LEFT)
    player2 = Player(pygame.K_UP, pygame.K_DOWN, stick_to=Player.RIGHT)
    ball = Ball(player1, player2)
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player1)
    all_sprites.add(player2)
    all_sprites.add(ball)
    return all_sprites, player1, player2, ball
