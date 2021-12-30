# arg must be a string
def interpret(arg: str) -> str:
    turing_machine = [0] * 100
    pointer = 0
    chars = []
    i = 0

    while i < len(arg):
        if turing_machine[pointer] > 255 or turing_machine[pointer] < 0:
            raise ValueError("Only int values between 0 and 255")

        elif arg[i] == '<':
            if pointer <= 0:
                raise MemoryError
            pointer -= 1

        elif arg[i] == '>':
            pointer += 1

        elif arg[i] == '+':
            turing_machine[pointer] += 1

        elif arg[i] == '-':
            if turing_machine[pointer] > 0:
                turing_machine[pointer] -= 1

        elif arg[i] == '.':
            chars.append(turing_machine[pointer])

        elif arg[i] == '[':
            # Skip over entirety of possible nested loops if value is 0
            if turing_machine[pointer] == 0:
                loop = 1
                while loop > 0:
                    i += 1
                    if arg[i] == '[':
                        loop += 1
                    elif arg[i] == ']':
                        loop -= 1

        elif arg[i] == ']':
            loop = 1
            while loop > 0:
                i -= 1
                if arg[i] == '[':
                    loop -= 1
                elif arg[i] == ']':
                    loop += 1
            i -= 1

        i += 1

    return_str = ""
    for i in chars:
        return_str += chr(i)
    return return_str
interpret.__doc__ = "A BrainF%@$ interpreter. Outputs ASCII string from bf input"
