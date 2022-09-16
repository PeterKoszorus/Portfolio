# Here will be all the constant values defined

# Instruction for the instruction set
INCREMENT = "00"
DECREMENT = "01"
JUMP = "10"
PRINT = "11"

# Maximum number of steps made by VirtualMachine to prevent infinite looping
MAX_STEPS = 500

# Letters definition for PRINT instruction
UP = "00"
DOWN = "01"
LEFT = "10"
RIGHT = "11"

# Global variables that define the movement for each tile
U = [-1, 0]
D = [1, 0]
L = [0, -1]
R = [0, 1]

# Global variable for the elite primates
ELITE = 2

# Mutation probability
MUTATION = 2
