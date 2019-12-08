import itertools

import intcode_computer.intcode_computer as ic

input_path = "input.txt"
with open(input_path) as input_file:
    intcode_program_str = input_file.read()
    intcode_program_list = [int(x) for x in intcode_program_str.split(sep=',')]

NUM_AMPS = 5
initial_state = intcode_program_list
# initial_state = [3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15, 15, 4, 15, 99, 0, 0]
# initial_state = [3, 26, 1001, 26, -4, 26, 3, 27, 1002, 27, 2, 27, 1, 27, 26, 27, 4, 27, 1001, 28, -1, 28, 1005, 28, 6, 99, 0, 0, 5]
# initial_state = [3, 52, 1001, 52, -5, 52, 3, 53, 1, 52, 56, 54, 1007, 54, 5, 55, 1005, 55, 26, 1001, 54,
#                  -5, 54, 1105, 1, 12, 1, 53, 54, 53, 1008, 54, 0, 55, 1001, 55, 1, 55, 2, 53, 55, 53, 4,
#                  53, 1001, 56, -1, 56, 1005, 56, 6, 99, 0, 0, 0, 0, 10]

phase_settings = list(itertools.permutations(x for x in range(5, 10)))
best_output = 0
for phase_setting in phase_settings:
    print(f"Testing settings {phase_setting}")
    amplifiers = []
    input_signal = 0
    for i in range(0, NUM_AMPS):
        new_amp = ic.IntcodeComputer(initial_state=initial_state, friendly_name=str(i))
        amplifiers.append(new_amp)
        res = next(new_amp.run_computer())
        assert res is True  # Computer asks for phase setting
        new_amp.next_input = phase_setting[i]
        res = next(new_amp.run_computer())
        assert res is True  # Computer asks for input signal

    finished_execution = False
    while finished_execution is False:
        for amp in amplifiers:
            amp.next_input = input_signal
            res = next(amp.run_computer())  # Run computer, until it produces an output
            assert type(res) is int  # Must provide an output value before new input/halt
            print(f"amplifier {amp.friendly_name} output {res}")
            input_signal = res

            res = next(amp.run_computer())  # Run again to find out if halting or requires a new input

            if res is False and amp is amplifiers[-1]:  # only halt all if its the last amp
                # Reached end of execution
                print(f"Reached end of execution of amp {amp.friendly_name} with last value")
                best_output = max(best_output, input_signal)
                finished_execution = True
                break
            assert type(res) is bool  # Computer asks for next input signal as it did not halt

print(f"Best output: {best_output}")
