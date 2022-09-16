# Here is the implementation of one primate


class Primate:

    def __init__(self, program, num_of_treasures):
        self.program = program
        self.num_of_treasures = num_of_treasures
        self.stats = None
        self.fitness = None

    # Method which changes the fitness of instruction set
    def set_fitness(self):
        self.fitness = self.calculate_fitness()

    # Method which stores the number of steps, and number of found treasures
    def set_stats(self, value):
        self.stats = value

    # This method calculates the fitness of each individual the less steps primate has the more fitter he is
    def calculate_fitness(self):
        if len(self.stats[0]) == 0:
            return 0
        if self.num_of_treasures == self.stats[1]:
            return None
        else:
            return (1 + (10 * self.stats[1])) - (len(self.stats[0]) * 0.001)
