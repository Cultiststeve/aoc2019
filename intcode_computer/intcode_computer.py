from typing import List

class IntcodeComputer:
    def __init__(self, initial_state: List[int] = None):
        self.state = initial_state

    def set_state(self, new_state: List[int]):
        self.state = new_state

    def run_computer(self):
        if self.state is None:
            raise Exception("Set state before running computer")

        for x in range(0, len(self.state), 4):
            # print(x)
            intcode = self.state[x]
            # print(intcode)
            if intcode == 1:
                # Addition
                self.state[self.state[x + 3]] = self.state[self.state[x + 1]] + \
                                                                    self.state[self.state[x + 2]]
            elif intcode == 2:
                # Multiplication
                self.state[self.state[x + 3]] = self.state[self.state[x + 1]] * \
                                                                    self.state[self.state[x + 2]]
            elif intcode == 99:
                # Halt
                return(f"Result: {self.state[0]}")
            else:
                raise RuntimeError(f"Encountered unrecognised opcode {intcode}")
            print(self.state)

    def set_noun(self, noun: int):
        self.state[1] = noun

    def set_verb(self, verb: int):
        self.state[2] = verb
