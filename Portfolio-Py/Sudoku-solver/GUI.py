import pygame

# screen settings
WIDTH = 560
HEIGHT = 620
FPS = 30

# colours
WHITE = [255, 255, 255]
BLACK = [0, 0, 0]
GRAY = [200, 200, 200]


def draw_grid(black, window):
    # vertical lines
    # [0] = x, [0] = y
    start_point = [60, 0]
    end_point = [60, 540]

    for n in range(8):
        pygame.draw.line(window, black, start_point, end_point)
        start_point[0] = start_point[0] + 60
        end_point[0] = start_point[0]


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
        draw_grid(BLACK, main_window)
        pygame.display.update()
        fps_clock.tick(FPS)


if __name__ == '__main__':
    main()
