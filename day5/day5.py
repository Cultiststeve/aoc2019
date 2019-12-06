import intcode_computer.intcode_computer as ic_c


input_path = "input.txt"

with open(input_path) as input_file:
    initial_state = input_file.read()


initial_state = initial_state.split(sep=',')
initial_state = [int(x) for x in initial_state]
# print(initial_state)

# initial_state = [1002,4,3,4,33]

computer = ic_c.IntcodeComputer()
computer.set_state(initial_state)

output = True
returns = []
while output is not False:
    output = next(computer.run_computer(input_val=1))
    returns.append(output)

print(returns)

print(computer._state)