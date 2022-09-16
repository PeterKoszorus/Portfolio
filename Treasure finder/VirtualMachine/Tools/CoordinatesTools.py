# Functions which are helping with the movement
from Util.Const import U, D, L, R


def move_coordinates(index, where, size):
    if where == "U":
        new_coordinates = [index[0] + U[0], index[1] + U[1]]
    elif where == "D":
        new_coordinates = [index[0] + D[0], index[1] + D[1]]
    elif where == "L":
        new_coordinates = [index[0] + L[0], index[1] + L[1]]
    elif where == "R":
        new_coordinates = [index[0] + R[0], index[1] + R[1]]
    else:
        return None
    if size[0] > new_coordinates[0] >= 0 and size[1] > new_coordinates[1] >= 0:
        return new_coordinates
    else:
        return None
