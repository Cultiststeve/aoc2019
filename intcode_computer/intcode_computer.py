from typing import List

class IntcodeComputer:
    def __init__(self, initial_state: List[int] = None):
        self.state = initial_state

    def set_state(self, new_state: List[int]):
        self.state = list.copy(new_state)

    def set_noun(self, noun: int):
        self.state[1] = noun

    def set_verb(self, verb: int):
        self.state[2] = verb

    def run_computer(self) -> int:
        # print(self.state)
        if self.state is None:
            raise Exception("Set state before running computer")

        for ip in range(0, len(self.state), 4):
            # print(x)
            intcode = self.state[ip]
            # print(intcode)
            if intcode == 1:
                # Addition
                self.state[self.state[ip + 3]] = self.state[self.state[ip + 1]] + \
                                                                    self.state[self.state[ip + 2]]
            elif intcode == 2:
                # Multiplication
                self.state[self.state[ip + 3]] = self.state[self.state[ip + 1]] * \
                                                                    self.state[self.state[ip + 2]]
            elif intcode == 99:
                # Halt
                return(self.state[0])
            else:
                raise RuntimeError(f"Encountered unrecognised opcode {intcode}")
            # print(self.state)
