import time

from intcode_computer import intcode_computer

input_path = "input.txt"
with open(input_path) as input_file:
    input_string = input_file.read()
    intcode_program_list = [int(x) for x in input_string.split(sep=',')]

computer = intcode_computer.IntcodeComputer(initial_state=intcode_program_list)

res = True
output = []
while res is not False:

    res = computer.run_computer()
    output.append(res)
    if res  is True:
        print("Needs input...")
        exit(0)


print(output)

total_blocks = 0
for i in range(2, len(output), 3):
    print(output[i])
    if output[i] == 3:
        print("Found paddle")
        time.sleep(2)
    elif output[i] == 2:
        total_blocks += 1

print(f"Total blocks: {total_blocks}")

