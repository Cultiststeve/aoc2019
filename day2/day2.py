import sys
import os
import intcode_computer.intcode_computer as ic
# input_path = "test1.txt"
input_path = "input.txt"

intcode_computer = ic.IntcodeComputer()

with open(input_path) as input_file:
    intcode_program_str = input_file.read()
    intcode_program_list = [int(x) for x in intcode_program_str.split(sep=',')]

    intcode_computer.set_state(intcode_program_list)

    if input_path == "input.txt":
        # Frig results as problem
        intcode_computer.set_noun(12)
        intcode_computer.set_verb(2)

    result = True
    res_list = []
    while result is not False:
        result = next(intcode_computer.run_computer())
        res_list.append(result)
    print(f"Part 1 result: {res_list}")

    print (intcode_computer._state[0])

    # # Part 2
    # for noun in range(0, 100):
    #     for verb in range(0, 100):
    #         print(f"Noun: {noun}, Verb: {verb}")
    #         intcode_computer.set_state(intcode_program_list)
    #         intcode_computer.set_noun(noun)
    #         intcode_computer.set_verb(verb)
    #         res = intcode_computer.run_computer()
    #
    #         if res == 19690720:
    #             print(100*noun + verb)
    #             exit(0)
    #
