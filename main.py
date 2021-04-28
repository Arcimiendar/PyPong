import pygame

HEIGHT = 450
WIDTH = 400

# ACC = 0.5
# FRIC = -0.12
# FPS = 60


def main():
    pygame.init()

    # frame_per_sec = pygame.time.Clock()

    display_surface = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("PyPong")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        # pygame.display.update()
        # frame_per_sec.tick(FPS)

    pygame.quit()


if __name__ == '__main__':
    main()
