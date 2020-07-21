def print_grid(grid):
    for x in range(9):
        for y in range(9):
            print(grid[x][y], end=" ")
        print(" ")


def row_check(grid, row, entry):
    for x in grid[row]:
        print(x)
        if x == entry:
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

print(row_check(SUDOKU_GRID, 0, 2))
