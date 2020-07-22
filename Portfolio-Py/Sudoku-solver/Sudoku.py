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


def check_box(grid, entry, row, line):
    for x in range(3):
        print(" ")
        for y in range(3):
            print(grid[x][y], end=" ")
            if entry == grid[x][y]:
                return False
    return True


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
print(check_box(SUDOKU_GRID, 7))
print(line_check(SUDOKU_GRID, 0, 1))
