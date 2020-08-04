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

# other vars
point_zero = [0, 0]
sudoku_grid = [[1, 2, 3, 4, 5, 6, 7, 8, 9],
               [2, 7, 0, 0, 3, 0, 0, 9, 0],
               [3, 0, 0, 9, 0, 0, 4, 0, 0],
               [4, 0, 0, 6, 0, 0, 2, 0, 0],
               [5, 1, 0, 0, 5, 0, 0, 4, 0],
               [6, 0, 6, 0, 0, 1, 0, 0, 7],
               [7, 0, 8, 0, 0, 6, 0, 0, 3],
               [8, 2, 0, 0, 8, 0, 0, 7, 0],
               [9, 0, 0, 2, 0, 0, 8, 0, 0]]


def where_am_i():
    x = point_zero[0] / 60
    y = point_zero[1] / 60
    return x, y


def draw_grid(black, window, font):
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

    # drawing num
    xy = [20, 10]
    for row in range(len(sudoku_grid)):
        for col in range(len(sudoku_grid)):
            num = sudoku_grid[col][row]
            text_to_screen(str(num), window, font, BLACK, xy[0], xy[1])
            xy[0] = xy[0] + 60
        xy[1] = xy[1] + 60


def movement(red, window, key, start_pos):
    SIZE = [60, 60]

    # left
    if key == 1:
        if start_pos[0] <= 0:
            pass
        else:
            start_pos[0] = start_pos[0] - 60
    # up
    elif key == 2:
        if start_pos[1] <= 0:
            pass
        else:
            start_pos[1] = start_pos[1] - 60

    # right
    elif key == 3:
        if start_pos[0] == 480:
            pass
        else:
            start_pos[0] = start_pos[0] + 60

    # down
    elif key == 4:
        if start_pos[1] == 480:
            pass
        else:
            start_pos[1] = start_pos[1] + 60

    # drawing
    else:
        pygame.draw.rect(window, red, (start_pos, SIZE), 4)


def text_to_screen(msg, window, font, color, x_pos, y_pos):
    txt_window = font.render(msg, False, color)
    window.blit(txt_window, (x_pos, y_pos))


def grid_change(num):
    sudoku_grid[int(where_am_i()[0])][int(where_am_i()[1])] = num


def main():
    pygame.init()

    fps_clock = pygame.time.Clock()
    main_window = pygame.display.set_mode((WIDTH, HEIGHT))
    font = pygame.font.SysFont(None, 60)

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
                    movement(RED, main_window, 1, point_zero)
                if event.key == pygame.K_UP:
                    movement(RED, main_window, 2, point_zero)
                if event.key == pygame.K_RIGHT:
                    movement(RED, main_window, 3, point_zero)
                if event.key == pygame.K_DOWN:
                    movement(RED, main_window, 4, point_zero)
                if event.key == pygame.K_KP0:
                    grid_change(0)
                if event.key == pygame.K_KP1:
                    grid_change(1)
                if event.key == pygame.K_KP2:
                    grid_change(2)
                if event.key == pygame.K_KP3:
                    grid_change(3)
                if event.key == pygame.K_KP4:
                    grid_change(4)
                if event.key == pygame.K_KP5:
                    grid_change(5)
                if event.key == pygame.K_KP6:
                    grid_change(6)
                if event.key == pygame.K_KP7:
                    grid_change(7)
                if event.key == pygame.K_KP8:
                    grid_change(8)
                if event.key == pygame.K_KP9:
                    grid_change(9)

        main_window.fill(WHITE)
        movement(RED, main_window, 0, point_zero)
        draw_grid(BLACK, main_window, font)
        pygame.display.flip()
        fps_clock.tick(FPS)


if __name__ == '__main__':
    main()
