from typing import List


class IntcodeComputer:
    def __init__(self, initial_state: List[int] = None):
        self._state = initial_state
        self._ip = 0

    def set_state(self, new_state: List[int]):
        self._state = list.copy(new_state)

    def set_noun(self, noun: int):
        self._state[1] = noun

    def set_verb(self, verb: int):
        self._state[2] = verb

    def run_computer(self, input_val: int = None) -> int:
        """
        Runs through current state

        On input, puts given value in then returns True indicating more to do

        Args:
            input_val:

        Returns:
            True if has just done an input command, and more work to do
            Value if has processed an output command
            False if reached a halt (99 op code)

        """
        # print(self.state)
        if self._state is None:
            raise Exception("Set state before running computer")

        while True:
            # print(x)
            instruction = str(self._state[self._ip])
            opcode = int(instruction[-2:])

            if opcode in {1, 2, 4}:
                # Opcodes with at least 1 parameter
                params = []
                for i in range(0, len(instruction) - 2):
                    params.append(int(instruction[i]))
                params.reverse()  # now param 1 is as position 0

                if len(params) >= 1 and params[0] == 1:  # immediate mode
                    param_1 = self._state[self._ip + 1]
                else:
                    param_1 = self._state[self._state[self._ip + 1]]

                if opcode in {1, 2}:
                    # Opcodes with 2 params
                    if len(params) >= 2 and params[1] == 1:  # immediate mode
                        param_2 = self._state[self._ip + 2]
                    else:
                        param_2 = self._state[self._state[self._ip + 2]]

                    if len(params) >= 3:
                        assert params[2] == 0

                assert len(params) <= 3

            if opcode == 1:
                # Addition
                self._state[self._state[self._ip + 3]] = param_1 + param_2
                self._ip += 4
            elif opcode == 2:
                # Multiplication
                self._state[self._state[self._ip + 3]] = param_1 * param_2
                self._ip += 4
            elif opcode == 3:
                # Input
                if input_val is None:
                    raise RuntimeError("Program required an input but none was given")
                self._state[self._state[self._ip + 1]] = input_val
                self._ip += 2
                yield True

            elif opcode == 4:
                # Output
                output_val = param_1
                self._ip += 2
                yield output_val
            elif opcode == 99:
                # Halt
                yield False
            else:
                raise RuntimeError(f"Encountered unrecognised opcode {opcode}")
            # print(self.state)
