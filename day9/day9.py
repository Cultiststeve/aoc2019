input_path = "input.txt"
with open(input_path) as input_file:
    input_string = input_file.read()
    intcode_program_list = [int(x) for x in input_string.split(sep=',')]

from intcode_computer.intcode_computer import IntcodeComputer

ic = IntcodeComputer(initial_state=intcode_program_list)

res = True
output = []
while res is not False:
    res = ic.run_computer()
    output.append(res)
    if res is True:
        ic.next_input = 2

print(output)