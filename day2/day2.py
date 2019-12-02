input_path = "test1.txt"
input_path = "input.txt"

with open(input_path) as input_file:
    intcode_program_str = input_file.read()
    intcode_program_list = [int(x) for x in intcode_program_str.split(sep=',')]

    if input_path == "input.txt":
        # Frig results as problem
        intcode_program_list[1] = 12
        intcode_program_list[2] = 2

    print(intcode_program_list)
    for x in range(0, len(intcode_program_list), 4):
        # print(x)
        intcode = intcode_program_list[x]
        # print(intcode)
        if intcode == 1:
            # Addition
            intcode_program_list[intcode_program_list[x+3]] = intcode_program_list[intcode_program_list[x+1]] + intcode_program_list[intcode_program_list[x+2]]
        elif intcode == 2:
            # Multiplication
            intcode_program_list[intcode_program_list[x+3]] = intcode_program_list[intcode_program_list[x+1]] * intcode_program_list[intcode_program_list[x+2]]
        elif intcode == 99:
            # Halt
            print(f"Result: {intcode_program_list[0]}")
            exit(0)
        else:
            raise RuntimeError(f"Encounted unrecognised opcode {intcode}")
        print(intcode_program_list)

