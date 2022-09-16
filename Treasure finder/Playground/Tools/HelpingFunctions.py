# Helping function which helps to find the index of given element in 2d list
def find_element_on_index(grid, element):
    for row in range(len(grid)):
        for column, value in enumerate(grid[row]):
            if element == value:
                return row, column
    return None
