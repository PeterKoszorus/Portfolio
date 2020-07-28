import pygame
from sudoku_solver import print_grid
# screen settings
WIDTH = 560
HEIGHT = 620
FPS = 30

# colours
WHITE = [255, 255, 255]
BLACK = [0, 0, 0]
GRAY = [200, 200, 200]


def main():
    pygame.init()

    fps_clock = pygame.time.Clock()
    main_window = pygame.display.set_mode((WIDTH, HEIGHT))

    main_window.fill(WHITE)
    pygame.display.set_caption("Sudoku")
    pygame.display.set_icon(pygame.image.load("Logo.png"))

    run = True
    # Main loop
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        pygame.display.update()
        fps_clock.tick(FPS)


if __name__ == '__main__':
    main()
