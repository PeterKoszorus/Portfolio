# This function converts hex to dec
# Arg: hexadecimal is expected as string
def ToDec(hexadecimal):
    hexadecimal = hexadecimal[::-1]
    exponent = 0
    total = 0

    for num in hexadecimal:

        if num == "a":
            num = "10"
        elif num == "b":
            num = "11"
        elif num == "c":
            num = "12"
        elif num == "d":
            num = "13"
        elif num == "e":
            num = "14"
        elif num == "f":
            num = "15"

        total = total + (pow(16, exponent) * int(num))
        exponent += 1

    return total
