import pygame

# screen settings
WIDTH = 540
HEIGHT = 620
FPS = 60

# colours
WHITE = [255, 255, 255]
BLACK = [0, 0, 0]
GRAY = [200, 200, 200]
RED = [255, 0, 0]


def draw_grid(black, window):
    # vertical lines
    # [0] = x, [0] = y
    start_point = [0, 0]
    end_point = [0, 540]

    for n in range(10):
        if n % 3 == 0:
            pygame.draw.line(window, black, start_point, end_point, 3)
        else:
            pygame.draw.line(window, black, start_point, end_point)
        start_point[0] = start_point[0] + 60
        end_point[0] = start_point[0]

    # horizontal lines
    start_point = [0, 0]
    end_point = [540, 0]

    for n in range(10):
        if n % 3 == 0:
            pygame.draw.line(window, black, start_point, end_point, 3)
        else:
            pygame.draw.line(window, black, start_point, end_point)
        start_point[1] = start_point[1] + 60
        end_point[1] = start_point[1]


point_zero = [0, 0]


def draw_rect(red, window, key, start_pos):
    SIZE = [60, 60]

    # first cube
    if key == 0:
        pygame.draw.rect(window, red, (start_pos, SIZE), 3)
    # left
    if key == 1:
        start_pos[0] = start_pos[0] - 60
        pygame.draw.rect(window, red, (start_pos, SIZE), 3)
    # up
    if key == 2:
        start_pos[1] = start_pos[1] - 60
        pygame.draw.rect(window, red, (start_pos, SIZE), 3)
    # right
    if key == 3:
        start_pos[0] = start_pos[0] + 60
        pygame.draw.rect(window, red, (start_pos, SIZE), 3)
    # down
    if key == 4:
        start_pos[1] = start_pos[1] + 60
        pygame.draw.rect(window, red, (start_pos, SIZE), 3)


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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    draw_rect(RED, main_window, 1, point_zero)
                if event.key == pygame.K_UP:
                    draw_rect(RED, main_window, 2, point_zero)
                if event.key == pygame.K_RIGHT:
                    draw_rect(RED, main_window, 3, point_zero)
                if event.key == pygame.K_DOWN:
                    draw_rect(RED, main_window, 4, point_zero)

        draw_grid(BLACK, main_window)
        draw_rect(RED, main_window, 0, point_zero)
        pygame.display.update()
        fps_clock.tick(FPS)


if __name__ == '__main__':
    main()
