import itertools

import intcode_computer.intcode_computer as ic

NUM_AMPS = 5
initial_state = [3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15, 15, 4, 15, 99, 0, 0]

amplifiers = []

phase_settings = list(itertools.permutations([0,1,2,3,4]))

input_signal = 0
best_output = 0
for phase_setting in phase_settings:
    for i in range(0, NUM_AMPS):
        new_amp = ic.IntcodeComputer(initial_state = initial_state)
        res = next(new_amp.run_computer())
        assert res is True  # Computer asks for phase setting
        new_amp.next_input = phase_setting[i]
        res = next(new_amp.run_computer())
        assert res is True  # Computer asks for phase setting
        new_amp.next_input = input_signal
        res = next(new_amp.run_computer())
        assert res is not True or False
        input_signal = res
    best_output = max(best_output, input_signal)
    input_signal = 0
print(f"Best output: {best_output}")