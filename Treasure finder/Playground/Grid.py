# Here is the implementation of grid
import random
from Playground.Tools.HelpingFunctions import find_element_on_index


class Grid:

    def __init__(self, size, num_of_treasures, grid):
        self.size = size
        self.num_of_treasures = num_of_treasures
        self.grid = self.generate_grid(grid)
        self.starting_position = find_element_on_index(self.grid, "S")

    # This method generates new grid
    def generate_grid(self, grid):
        if grid:
            return grid

        new_grid = [["X" for y in range(self.size[0])] for x in range(self.size[1])]

        # Selecting random start position
        new_grid[random.randint(0, (self.size[1] - 1))][random.randint(0, (self.size[0] - 1))] = "S"

        # Here I m randomly selecting the places for treasure
        i = 0
        while i < self.num_of_treasures:
            y = random.randint(0, (self.size[1] - 1))
            x = random.randint(0, (self.size[0] - 1))

            if new_grid[y][x] != "S" and new_grid[y][x] != "P":
                new_grid[y][x] = "P"
                i += 1

        return new_grid

    # This method prints the grid
    def print_grid(self):
        print("PRINTING OUT THE PLAYING AREA")
        for row in range(len(self.grid)):
            print("|", end="")
            for value in self.grid[row]:
                print(value, end="|")
            print()
        print()