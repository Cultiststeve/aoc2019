import intcode_computer.intcode_computer as ic_c


input_path = "input.txt"

with open(input_path) as input_file:
    initial_state = input_file.read()


initial_state = initial_state.split(sep=',')
initial_state = [int(x) for x in initial_state]
# print(initial_state)

# initial_state = [1002,4,3,4,33]
# initial_state = [3,9,8,9,10,9,4,9,99,-1,8]  # equals to 8 positional
# initial_state = [3,9,7,9,10,9,4,9,99,-1,8]  # less than 8 positional
# initial_state = [3,3,1108,-1,8,3,4,3,99]  # equal 8, imediate
# initial_state = [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
# 1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
# 999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99]  # input, outpout is += 8

computer = ic_c.IntcodeComputer()
computer.set_state(initial_state)

output = True
returns = []
while output is not False:
    output = next(computer.run_computer(input_val=5))
    returns.append(output)

print(returns)

print(computer._state)