import math
import time

input_path = "input.txt"
signal_received = []
with open(input_path) as input_file:
    input_string = input_file.read()

# input_string = "12345678"  # Example

first_seven = input_string[:7]
print(first_seven)
msg_offset = int(first_seven)

print(f"msg len is {len(input_string)}")
for i in range(0, 100):
    for char in input_string:
        if char == '\n':
            break
        signal_received.append(int(char))
print(f"modified len is {len(signal_received)}")


print(f"Got a signal of length {len(signal_received)}")
print(f"Signal: {signal_received}")

current_signal_list = signal_received.copy()
FTT_PHASES = 100
BASE_PATTERN = [0, 1, 0, -1]

for phase_i in range(0, FTT_PHASES):
    initial_time = time.time()
    print(f"\n!!!!!!\nOn FTT phase {phase_i}")
    assert len(current_signal_list) == len(signal_received)
    new_signal = [None] * len(current_signal_list)
    # print(f"new signal: {new_signal}")

    for element_i in range(0, len(current_signal_list)):
        # print(f"------\n\nElement {element_i} in current signal")

        repeating_pattern = []
        for base_pat_i in range(0, len(BASE_PATTERN)):
            for _ in range(0, element_i+1):  # Each element of pattern repeats equal to element_i
                repeating_pattern.append(BASE_PATTERN[base_pat_i])
        # print(f"Repeating pattern: {repeating_pattern}")

        # Make sure repeating pattern covers the length of signal
        while len(repeating_pattern) < len(current_signal_list) + 1:  # (+1 for first skipped element)
            repeating_pattern += repeating_pattern
        repeating_pattern = repeating_pattern[1:]  # skip first value exactly once
        # print(f"Expanded repeating pattern: {repeating_pattern}")

        new_element_total = 0
        for sum_element_i in range(0, len(current_signal_list)):
            # print(f"{current_signal_list[sum_element_i]}*{repeating_pattern[sum_element_i]} + ",end='')
            new_element_total += current_signal_list[sum_element_i] * repeating_pattern[sum_element_i]
        # print("")

        new_element_total = abs(new_element_total)
        # print(f"New element total is {new_element_total}")

        if new_element_total >= 10:
            new_element_total = new_element_total - (math.floor(new_element_total / 10) * 10)
        # print(f"New element total is {new_element_total}")
        new_signal[element_i] = new_element_total

    current_signal_list = new_signal
    print(f"New current signal is {current_signal_list}")
    print(f"Took {time.time() - initial_time} seconds to process this phase.")

print(f"Output signal is: {current_signal_list}")
print(f"Output signal length is {len(current_signal_list)}")

print(f"With offset, 8 8 didg message is {current_signal_list[msg_offset:msg_offset+8]}")
