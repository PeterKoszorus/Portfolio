def print_grid(grid):
    for x in range(9):
        for y in range(9):
            print(grid[x][y], end=" ")
        print(" ")


def row_check(grid, row, entry):
    for i in range(9):
        if grid[row][i] == entry:
            return False
    return True


def line_check(grid, line, entry):
    for i in range(9):
        if grid[i][line] == entry:
            return False
    return True


def find_zero(grid, xy):
    for row in range(9):
        for line in range(9):
            if grid[row][line] == 0:
                xy[0] = row
                xy[1] = line
                return True


def check_box(grid, entry, box_num):
    row = box_num[0]
    line = box_num[1]

    for x in range(3):
        print(" ")
        for y in range(3):
            print(grid[x + row][y + line], end=" ")
            if entry == grid[x + row][y + line]:
                return False
    return True


def which_box(row, line):
    box_num = [0, 0]

    if row < 3 and line < 3:
        box_num = [0, 0]
    elif row < 3 and line < 6:
        box_num = [0, 3]
    elif row < 3 and line < 9:
        box_num = [0, 6]
    elif row < 6 and line < 3:
        box_num = [3, 0]
    elif row < 6 and line < 6:
        box_num = [3, 3]
    elif row < 6 and line < 9:
        box_num = [3, 6]
    elif row < 9 and line < 3:
        box_num = [6, 0]
    elif row < 9 and line < 6:
        box_num = [6, 3]
    elif row < 9 and line < 9:
        box_num = [6, 6]

    return box_num

SUDOKU_GRID = [[3, 0, 6, 5, 0, 8, 4, 0, 0],
               [5, 2, 0, 0, 0, 0, 0, 0, 0],
               [0, 8, 7, 0, 0, 0, 0, 3, 1],
               [0, 0, 3, 0, 1, 0, 0, 8, 0],
               [9, 0, 0, 8, 6, 3, 0, 0, 5],
               [0, 5, 0, 0, 9, 0, 6, 0, 0],
               [1, 3, 0, 0, 0, 0, 2, 5, 0],
               [0, 0, 0, 0, 0, 0, 0, 7, 4],
               [0, 0, 5, 2, 0, 6, 3, 0, 0]]

xy = [0,0]
find_zero(SUDOKU_GRID, xy)
for num in xy:
    print(num)
print(check_box(SUDOKU_GRID, 1, which_box(3, 3)))
print(line_check(SUDOKU_GRID, 0, 1))
