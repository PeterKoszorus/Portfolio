import math
import random
import numpy as np

from Playground.Grid import Grid as Gd
from Primate.Primate import Primate as Pr
from Util.Const import MAX_STEPS, ELITE, MUTATION
from VirtualMachine.Tools.InstructionSet import InstructionSet as Is
from VirtualMachine.VirtualMachine import VirtualMachine as Vm


def main():
    breeding_mod = input("Select which method do you wanna you use to breed the generation Tourney/Roulette  ")
    num = input("Enter the number of primates in generation: ")
    num_of_generations = input("How many generations would you like to create: ")
    size = input("Enter the size of playing area: ")
    num_of_treasures = input("Enter a number of treasures: ")

    grid = None

    # # Testing grid to get consistent test results 7x7 5 treasures
    # grid = [["X", "X", "X", "X", "X", "X", "X"],
    #         ["X", "X", "X", "X", "P", "X", "X"],
    #         ["X", "X", "P", "X", "X", "X", "X"],
    #         ["X", "X", "X", "X", "X", "X", "P"],
    #         ["X", "P", "X", "X", "X", "X", "X"],
    #         ["X", "X", "X", "X", "P", "X", "X"],
    #         ["X", "X", "X", "S", "X", "X", "X"]]

    size = tuple(int(x) for x in size.split(" "))
    playing_area = Gd(size, int(num_of_treasures), grid)
    playing_area.print_grid()

    virtual_machine = Vm(MAX_STEPS, playing_area)

    generation = create_generation(int(num), playing_area.num_of_treasures)

    counter = 1

    while True:
        while counter <= int(num_of_generations):
            if run_gen(generation, virtual_machine, counter) is not True:
                counter += 1
                if counter <= int(num_of_generations):
                    generation = breed(generation, playing_area.num_of_treasures, breeding_mod)
            else:
                print("{}{}{}".format("The solution was found in: ", counter, " generation"))
                return None

        print("The solution wasn't found")
        temp = sorted(generation, key=lambda x: x.fitness, reverse=True)
        print("{}{}".format("The best solution found was: ", temp[0].stats[0]))
        print("{}{}".format("Fitness of best solution: ", temp[0].fitness))
        print("{}{}".format("Number of found treasure: ", temp[0].stats[1]))

        cont = input("Would you like to continue the search ? Y/N  ")
        if cont == "N":
            return None
        num_of_generations = input("How many generations would you like to try ?  ")
        num_of_generations = counter + int(num_of_generations) - 1


# This function will sort out the breeding process
def breed(generation, num_of_treasures, breeding_method):
    # This handles the elite primates
    num_of_elite = math.floor((len(generation) / 100) * ELITE)
    temp = sorted(generation, key=lambda x: x.fitness, reverse=True)
    new_gen = [] + temp[0: num_of_elite]

    # This handles the rest of the generation
    for num in range(len(generation) - num_of_elite):
        if breeding_method == "Tourney":
            new_gen.append(Pr(Is(crossover(tourney(generation), tourney(generation))), num_of_treasures))
        elif breeding_method == "Roulette":
            new_gen.append(Pr(Is(crossover(roulette(generation), roulette(generation))), num_of_treasures))
        if random.randint(0, 100) < MUTATION:
            mutation(new_gen[-1])
    return new_gen


# Function which mutates flips one bit in the whole instruction set
def mutation(primate):
    memory_block = random.randint(0, len(primate.program.instruction_set) - 1)
    bit_num = random.randint(0, len(primate.program.instruction_set[memory_block]) - 1)

    original_string = list(primate.program.instruction_set[memory_block])

    if original_string[bit_num] == "0":
        original_string[bit_num] = "1"
    elif original_string[bit_num] == "1":
        original_string[bit_num] = "0"

    primate.program.instruction_set[memory_block] = ''.join(original_string)


# This will return a child gene made by crossing two parents
def crossover(parent1, parent2):
    starting_index = random.randint(0, (len(parent1.program.instruction_set) - 33))

    child_gene = []
    for index in range(64):
        if index < starting_index:
            child_gene.append(parent2.program.instruction_set[index])
        elif starting_index <= index < starting_index + 32:
            child_gene.append(parent1.program.instruction_set[index])
        else:
            child_gene.append(parent2.program.instruction_set[index])

    return child_gene


# Function which chooses one individual by the tournament selection
def tourney(gen):
    selected_individuals = [random.choice(gen)]
    i = 0

    # Selecting three candidates for the tourney
    while i < 2:
        temp = random.choice(gen)
        if temp not in selected_individuals:
            selected_individuals.append(temp)
            i += 1

    # Taking the strongest individual
    selected_individuals.sort(key=lambda x: x.fitness, reverse=True)

    return selected_individuals[0]


# Function which selects individual by the roulette selection process
def roulette(gen):
    gen_fitness = sum(x.fitness for x in gen)
    primate_chance = [x.fitness/gen_fitness for x in gen]

    return np.random.choice(gen, p=primate_chance)


# Loop for running the whole generation
def run_gen(generation, virtual_machine, counter):
    average_fit = 0
    average_treasure = 0
    for primate in generation:
        temp = virtual_machine.run_program(primate.program)
        primate.set_stats(temp)
        primate.set_fitness()
        if temp is not None:
            fitness = primate.fitness
            if fitness is None:
                print("Solution was found!")
                print("{}{}".format("Steps: ", temp[0]))
                return True
            average_fit = fitness + average_fit
            average_treasure = temp[1] + average_treasure

    print("-------------------------------------------")
    print("{}{}".format("GENERATION NUMBER: ", counter))
    print("{}{}".format("AVERAGE FITNESS OF GENERATION:", average_fit / len(generation)))
    print("{}{}".format("AVERAGE NUMBER OF TREASURES FOUND:", average_treasure / len(generation)))
    print("-------------------------------------------")
    print()

    return False


# Create the initial generation
def create_generation(num_of_primates, num_of_treasures):
    generation = []
    for i in range(num_of_primates):
        generation.append(Pr(Is(None), num_of_treasures))
    if generation:
        return generation
    else:
        return None


if __name__ == '__main__':
    main()

