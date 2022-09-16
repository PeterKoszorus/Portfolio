# Here will be the implementation of instruction set generator
import random
from Util.Const import INCREMENT, DECREMENT, JUMP, PRINT


# This function generates the instruction set
def generate_instruction_set(instructions):

    if instructions is not None:
        return instructions

    select_from = "01"
    instruction_set = []

    for i in range(64):

        instruction = ''.join((random.choice(select_from)) for x in range(8))
        instruction_set.append(instruction)

    if instruction_set:
        return instruction_set
    else:
        return None


class InstructionSet:

    def __init__(self, instructions):
        self.instruction_set = generate_instruction_set(instructions)

    # Method which lets me print the whole instruction set and also prints what should be done
    def print_instruction_set(self):
        print("Printing the instruction set of this primate")
        for instruction in self.instruction_set:
            if instruction[:2] == INCREMENT:
                print("{} {}".format(instruction, " INCREMENTING"))
            elif instruction[:2] == DECREMENT:
                print("{} {}".format(instruction, " DECREMENTING"))
            elif instruction[:2] == JUMP:
                print("{} {}".format(instruction, " JUMPING"))
            elif instruction[:2] == PRINT:
                print("{} {}".format(instruction, " PRINTING"))
