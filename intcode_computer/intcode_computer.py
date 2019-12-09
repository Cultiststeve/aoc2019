from typing import List


class IntcodeComputer:
    def __init__(self,
                 initial_state: List[int] = None,
                 friendly_name : str = None):
        self._state = None
        if initial_state:
            self.set_state(initial_state)
        self._ip = 0
        self._relative_base = 0
        self.next_input = None
        if friendly_name:
            self.friendly_name = friendly_name

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
            9: {"name": "relative-base-ofset",
                "func": self._relative_base_offset,
                "num_params": 1,
                "steps_foward": 2
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

    def run_computer(self) -> iter:
        """
        Runs through current state

        On input, puts given value in then returns True indicating more to do

        Yields:
            True if computer requires an input
            Value if has processed an output command
            False if reached a halt (99 op code)

        """
        # print(self.state)
        if self._state is None:
            raise Exception("Set state before running computer")

        while True:
            instruction = str(self._state[self._ip])
            opcode = int(instruction[-2:])

            if opcode not in self.valid_opcodes:
                raise Exception(f"Opcode {opcode} not in recognised valid codes")

            params = []
            for i in range(1, self.valid_opcodes[opcode]["num_params"] + 1):
                # For each parameter of the opcode
                try:
                    # Extract mode from initial instruction
                    param_mode = int(instruction[-2 - i:-2 - i + 1])
                    assert param_mode in self.param_modes
                except (IndexError, ValueError):
                    # If not specified, default mode is 0
                    param_mode = 0

                # self._ip + i  = position of parameter in intcode
                # self._state[self._ip + i] = value of parameter
                # self._state[self._state[self._ip + i]] = value at position of [value of parameter]

                if param_mode == 0:
                    # position mode, so the parameter is the value of the state, at the position the parameter points to
                    # parameter is found at the IP (current instruction) + parameter number
                    params.append(self._state[self._state[self._ip + i]])
                elif param_mode == 1:
                    # immediate mode, param value is where the IP points to
                    params.append(self._state[self._ip + i])
                elif param_mode == 2:
                    # Relative mode - position mode but [value of parameter is modified by the rel-base
                    params.append(self._state[self._state[self._ip + i] + self._relative_base])
                else:
                    raise RuntimeError(f"Invalid param mode : {param_mode}")

            res = self.valid_opcodes[opcode]["func"](params)
            if res is not True:  # Dont increase ip if we didnt carry out input because none was present
                self._ip += self.valid_opcodes[opcode]["steps_foward"]
            if res is not None:
                # if calculation returned something then need to pause execution to inform
                # False = 99, end of program
                # True = requesting an input
                # integers = value to output
                return res

    def _addition(self, params: List[int]):
        """
        output / 3rd param is always positional mode, so its just assumed for all the funcs,
        no need for parsed 3rd param
        """
        assert len(params) is 3
        self._state[self._state[self._ip + 3]] = params[0] + params[1]
        return None

    def _multiplication(self, params: List):
        assert len(params) is 3
        self._state[self._state[self._ip + 3]] = params[0] * params[1]
        return None

    def _input(self, params: List[int]):
        assert len(params) is 1
        if self.next_input is None:
            return True
        self._state[self._state[self._ip + 1]] = self.next_input
        self.next_input = None
        return None

    def _output(self, params: List):
        assert len(params) is 1
        output_val = params[0]
        return output_val

    def _jump_if_true(self, params: List):
        assert len(params) is 2
        if params[0] != 0:
            self._ip = params[1] - 3
        return None

    def _jump_if_false(self, params: List):
        assert len(params) is 2
        if params[0] == 0:
            self._ip = params[1] - 3
        return None

    def _less_than(self, params: List):
        assert len(params) is 3
        if params[0] < params[1]:
            self._state[self._state[self._ip + 3]] = 1
        else:
            self._state[self._state[self._ip + 3]] = 0
        return None

    def _equals(self, params: List):
        assert len(params) is 3
        if params[0] == params[1]:
            self._state[self._state[self._ip + 3]] = 1
        else:
            self._state[self._state[self._ip + 3]] = 0
        return None

    def _relative_base_offset(self, params: List):
        assert len(params) is 1
        self._relative_base +=params[0]
        return None

    def _end(self, params: List):
        assert len(params) is 0
        return False
