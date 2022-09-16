# This class is responsible for running the instruction set
from Util.Const import INCREMENT, DECREMENT, JUMP, PRINT, UP, DOWN, LEFT, RIGHT
from VirtualMachine.Tools.CoordinatesTools import move_coordinates
import copy


class VirtualMachine:

    def __init__(self, limit, playing_area):
        self.limit = limit
        self.playing_area = playing_area

    # This method will check if the given steps give you the solution
    def check_solution(self, steps):

        actual_pos = self.playing_area.starting_position
        found_treasure = 0
        already_visited = []

        for direction in steps:
            temp = move_coordinates(actual_pos, direction, self.playing_area.size)
            if temp is not None:
                if self.playing_area.grid[temp[0]][temp[1]] == "P" and temp not in already_visited:
                    found_treasure += 1
                    already_visited.append(temp)
                actual_pos = temp
                if found_treasure == self.playing_area.num_of_treasures:
                    return True, found_treasure
            elif temp is None:
                return False, found_treasure
        return None, found_treasure

    # This method runs the program
    def run_program(self, og_program):
        program = copy.deepcopy(og_program.instruction_set)
        steps = []
        i = 0
        counter = 0

        while i < 64 and counter < self.limit:

            if steps:
                solution = self.check_solution(steps)
                if solution[0]:
                    return steps, solution[1]
                elif solution[0] is False:
                    steps.pop()
                    return steps, solution[1]

            instruction = program[i][:2]

            if instruction == INCREMENT:
                # This operation increments the instruction
                program[i] = int(program[i], 2)
                program[i] += 1
                program[i] = f'{program[i]:0{8}b}'

                i += 1
                counter += 1

                continue
            if instruction == DECREMENT:
                # This operation decrements the instruction
                program[i] = int(program[i], 2)
                program[i] -= 1
                program[i] = f'{program[i]:0{8}b}'

                i += 1
                counter += 1

                continue
            if instruction == JUMP:
                where_to = int(program[i][2:], 2)
                if where_to > i:
                    i = (where_to - i) + i
                    counter += 1
                elif where_to < i:
                    i = (i - where_to) - i
                    counter += 1
                elif where_to == i:
                    counter += 1

                continue
            if instruction == PRINT:
                letter = program[i][-2:]
                if letter == UP:
                    steps.append("U")
                elif letter == DOWN:
                    steps.append("D")
                elif letter == LEFT:
                    steps.append("L")
                elif letter == RIGHT:
                    steps.append("R")

                i += 1
                counter += 1

                continue

        # When no treasure was found during the check up
        solution = self.check_solution(steps)
        return steps, solution[1]
