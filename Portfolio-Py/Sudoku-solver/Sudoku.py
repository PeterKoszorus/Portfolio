def print_grid(grid):
    for row in range(9):
        for col in range(9):
            print(grid[row][col], end=" ")
        print(" ")


def row_check(grid, row, entry):
    for i in range(9):
        if grid[row][i] == entry:
            return False
    return True


def line_check(grid, col, entry):
    for i in range(9):
        if grid[i][col] == entry:
            return False
    return True


def find_zero(grid, coordinates):
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                coordinates[0] = row
                coordinates[1] = col
                return True


def check_box(grid, entry, box_num):
    row = box_num[0]
    col = box_num[1]

    for n in range(3):
        for m in range(3):
            if entry == grid[n + row][m + col]:
                return False
    return True


def which_box(row, col):
    box_num = [0, 0]

    if row < 3 and col < 3:
        box_num = [0, 0]
    elif row < 3 and col < 6:
        box_num = [0, 3]
    elif row < 3 and col < 9:
        box_num = [0, 6]
    elif row < 6 and col < 3:
        box_num = [3, 0]
    elif row < 6 and col < 6:
        box_num = [3, 3]
    elif row < 6 and col < 9:
        box_num = [3, 6]
    elif row < 9 and col < 3:
        box_num = [6, 0]
    elif row < 9 and col < 6:
        box_num = [6, 3]
    elif row < 9 and col < 9:
        box_num = [6, 6]

    return box_num


def all_good(grid, row, col, entry):
    if row_check(grid, row, entry) and line_check(grid, col, entry) and check_box(grid, entry, which_box(row, col)):
        return True
    else:
        return False


SUDOKU_GRID = [[3, 0, 6, 5, 0, 8, 4, 0, 0],
               [5, 2, 0, 0, 0, 0, 0, 0, 0],
               [0, 8, 7, 0, 0, 0, 0, 3, 1],
               [0, 0, 3, 0, 1, 0, 0, 8, 0],
               [9, 0, 0, 8, 6, 3, 0, 0, 5],
               [0, 5, 0, 0, 9, 0, 6, 0, 0],
               [1, 3, 0, 0, 0, 0, 2, 5, 0],
               [0, 0, 0, 0, 0, 0, 0, 7, 4],
               [0, 0, 5, 2, 0, 6, 3, 0, 0]]

yx = [0, 0]
y = yx[0]
x = yx[1]
print(all_good(SUDOKU_GRID, y, x, 1))
print_grid(SUDOKU_GRID)
# dynamic range func by doing range(len(grid))
