def print_grid(grid):
    for row in range(len(grid)):
        for col in range(len(grid)):
            print(grid[row][col], end=" ")
        print(" ")


def row_check(grid, row, entry):
    for i in range(len(grid)):
        if grid[row][i] == entry:
            return False
    return True


def line_check(grid, col, entry):
    for i in range(len(grid)):
        if grid[i][col] == entry:
            return False
    return True


def find_zero(grid, coordinates):
    for row in range(len(grid)):
        for col in range(len(grid)):
            if grid[row][col] == 0:
                coordinates[0] = row
                coordinates[1] = col
                return True
    return False


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


def solve(grid):
    yx = [0, 0]

    if not find_zero(grid, yx):
        return True
    else:
        row = yx[0]
        col = yx[1]

    for num in range(1, 10):
        if all_good(grid, row, col, num):
            grid[row][col] = num

            if solve(grid):
                return True

            grid[row][col] = 0

    return False


def main():
    SUDOKU_GRID = [[0, 0, 9, 0, 0, 4, 0, 0, 1],
                   [0, 7, 0, 0, 3, 0, 0, 9, 0],
                   [8, 0, 0, 9, 0, 0, 4, 0, 0],
                   [9, 0, 0, 6, 0, 0, 2, 0, 0],
                   [0, 1, 0, 0, 5, 0, 0, 4, 0],
                   [0, 0, 6, 0, 0, 1, 0, 0, 7],
                   [0, 0, 8, 0, 0, 6, 0, 0, 3],
                   [0, 2, 0, 0, 8, 0, 0, 7, 0],
                   [5, 0, 0, 2, 0, 0, 8, 0, 0]]

    print_grid(SUDOKU_GRID)
    print(" ")
    if solve(SUDOKU_GRID):
        print_grid(SUDOKU_GRID)
    else:
        print("This sudoku has no solution")


if __name__ == '__main__':
    main()