import pygame.sprite

from constants import WIDTH, HEIGHT


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.orig_width, self.orig_height = int(WIDTH * 0.02), int(HEIGHT * 0.2)

        self.surf = pygame.Surface((self.orig_width, self.orig_height))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()

    def scale(self, window_width, window_height):
        width = int(self.orig_width * window_width / WIDTH)
        height = int(self.orig_height * window_height / HEIGHT)
        self.surf = pygame.transform.scale(self.surf, (width, height))
        self.surf.fill((255, 255, 255))


# class Ball(pygame.sprite.Sprite):
#     def __init__(self):
#         super(Ball, self).__init__()
#         self.surf = pygame.Surface((30, 30))
#         self.surf.fill((128, 255, 40))
#         self.rect = self.surf.get_rect()


def get_sprites():
    player = Player()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    return all_sprites
