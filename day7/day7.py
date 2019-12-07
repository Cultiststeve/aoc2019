import itertools

import intcode_computer.intcode_computer as ic

test_1_program = [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]
test_2 = [3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,
1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0]

input_path = "input.txt"
with open(input_path) as input_file:
    intcode_program_str = input_file.read()
    intcode_program_list = [int(x) for x in intcode_program_str.split(sep=',')]

class Amplifier:
    def __init__(self, name, input_signal, state):
        self.name = name
        self.input_signal = input_signal
        self.computer = ic.IntcodeComputer()
        self.computer.set_state(state)

    def compute_output(self, phase_setting: int):
        print(f"Running amp with input {phase_setting}")
        result = next(self.computer.run_computer(input_val=phase_setting))
        assert result is True
        print(f"Running amp with input {self.input_signal}")
        result = next(self.computer.run_computer(self.input_signal))
        assert result is True
        # Taken 2 inputs, now run till output
        result = next(self.computer.run_computer())

        output_signal = result
        return output_signal


num_amplifiers = 5
amplifiers = []
phase_settings = list(itertools.permutations([0,1,2,3,4,5]))
best_output = 0
for possible_setting in phase_settings:
    print(f"\n Trying settings {possible_setting}")
    input_signal = 0
    for i in range(0, num_amplifiers):
        amp = Amplifier(name=i, input_signal=input_signal, state=intcode_program_list)
        amplifiers.append(amp)

        res = amp.compute_output(phase_setting=possible_setting[i])
        print(f"Result of amp {i} is {res}")
        input_signal = res
    best_output = max(best_output, input_signal)

print(f"Best output: {best_output}")