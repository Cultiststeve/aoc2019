from typing import List


class IntcodeComputer:
    def __init__(self, initial_state: List[int] = None):
        self._state = None
        if initial_state:
            self.set_state(initial_state)
        self._ip = 0
        self.input_val = None

        self.valid_opcodes = {
            1: {"name": "addition",
                "func": self._addition,
                "num_params": 3,
                "steps_foward": 4
                },
            2: {"name": "multiplication",
                "func": self._multiplication,
                "num_params": 3,
                "steps_foward": 4
                },
            3: {"name": "input",
                "func": self._input,
                "num_params": 1,
                "steps_foward": 2
                },
            4: {"name": "output",
                "func": self._output,
                "num_params": 1,
                "steps_foward": 2
                },
            5: {"name": "jump-if-true",
                "func": self._jump_if_true,
                "num_params": 2,
                "steps_foward": 3
                },
            6: {"name": "jump-if-false",
                "func": self._jump_if_false,
                "num_params": 2,
                "steps_foward": 3
                },
            7: {"name": "less-than",
                "func": self._less_than,
                "num_params": 3,
                "steps_foward": 4
                },
            8: {"name": "equals",
                "func": self._equals,
                "num_params": 3,
                "steps_foward": 4
                },
            99: {"name": "end",
                 "func": self._end,
                 "num_params": 0,
                 "steps_foward": 0
                 }
        }

        self.param_modes = {0: "position",
                            1: "immediatee"}

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

        self.input_val = input_val

        while True:
            instruction = str(self._state[self._ip])
            opcode = int(instruction[-2:])

            if opcode not in self.valid_opcodes:
                raise Exception(f"Opcode {opcode} not in recognised valid codes")

            params = []
            for i in range(1, self.valid_opcodes[opcode]["num_params"] + 1):
                # For each paramter of the opcode
                try:
                    # Extract mode from initial instruction
                    param_mode = int(instruction[-2-i:-2-i+1])
                    assert param_mode in self.param_modes
                except (IndexError, ValueError):
                    param_mode = 0

                if param_mode == 0:
                    # position mode, so the paramter is the value of the state, at the position the IP points to
                    params.append(self._state[self._state[self._ip + i]])
                elif param_mode == 1:
                    # immediate mode, param value is where the IP points to
                    params.append(self._state[self._ip + i])
                else:
                    raise RuntimeError(f"Invalid param mode : {param_mode}")



            res = self.valid_opcodes[opcode]["func"](params)
            if res is not None:
                yield res

            self._ip += self.valid_opcodes[opcode]["steps_foward"]

    def _addition(self, params: List):
        self._state[self._state[self._ip+3]] = params[0] + params[1]
        return None

    def _multiplication(self, params: List):
        self._state[self._state[self._ip+3]] = params[0] * params[1]
        return None

    def _input(self, params: List[int]):
        if self.input_val is None:
            raise RuntimeError("Program required an input but none was given")
        self._state[self._state[self._ip + 1]] = self.input_val
        self._ip += 2
        return True

    def _output(self, params):
        output_val = params[0]
        self._ip += 2
        return output_val

    def _jump_if_true(self, params):
        if params[0] != 0:
            self._ip = params[1] - 3

    def _jump_if_false(self, params):
        if params[0] == 0:
            self._ip = params[1] - 3

    def _less_than(self, params):
        if params[0] < params[1]:
            self._state[self._state[self._ip+3]] = 1
        else:
            self._state[self._state[self._ip + 3]] = 0

    def _equals(self, params):
        if params[0] == params[1]:
            self._state[self._state[self._ip + 3]] = 1
        else:
            self._state[self._state[self._ip + 3]] = 0

    def _end(self, params):
        return False
