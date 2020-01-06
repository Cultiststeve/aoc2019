from typing import List


class IntcodeComputer:
    """
    Defines a functional 'intcode' computer for Advent of code 2019
    https://adventofcode.com

    Works as an interpreter for the intcode language created for the coding challenge

    The computer can be given an initial state or set at any point
    When ran, the computer processes opcodes until:
        input command, and no input is ready, in which case 'True' is returned
        output command, in which case the output value is returned
        halt command, in which case 'False' is returned

    # TODO logging
    """

    def __init__(self,
                 initial_state: List[int] = None,
                 friendly_name: str = None):
        self._state = None
        if initial_state:
            self.set_state(initial_state)
        self._ip = 0  # Instruction pointer
        self._relative_base = 0  # Relative base for [2] relative mode params
        # TODO make next_input into a queue
        self.next_input = None  # When processing input opcode, input is this var
        if friendly_name:
            self.friendly_name = friendly_name

        self.valid_opcodes = {
            1: {"name": "addition",
                "func": self._addition,
                "num_params": 3,
                "steps_forward": 4
                },
            2: {"name": "multiplication",
                "func": self._multiplication,
                "num_params": 3,
                "steps_forward": 4
                },
            3: {"name": "input",
                "func": self._input,
                "num_params": 1,
                "steps_forward": 2
                },
            4: {"name": "output",
                "func": self._output,
                "num_params": 1,
                "steps_forward": 2
                },
            5: {"name": "jump-if-true",
                "func": self._jump_if_true,
                "num_params": 2,
                "steps_forward": 3
                },
            6: {"name": "jump-if-false",
                "func": self._jump_if_false,
                "num_params": 2,
                "steps_forward": 3
                },
            7: {"name": "less-than",
                "func": self._less_than,
                "num_params": 3,
                "steps_forward": 4
                },
            8: {"name": "equals",
                "func": self._equals,
                "num_params": 3,
                "steps_forward": 4
                },
            9: {"name": "relative-base-offset",
                "func": self._relative_base_offset,
                "num_params": 1,
                "steps_forward": 2
                },
            99: {"name": "end",
                 "func": self._end,
                 "num_params": 0,
                 "steps_forward": 0
                 }
        }

        self.param_modes = {0: "position",
                            1: "immediate",
                            2: "relative"}

    def set_state(self, new_state: List[int], instruction_pointer=0):
        self._state = list.copy(new_state)
        self._ip = instruction_pointer

    def get_memory_location(self, location: int):
        assert location >= 0
        try:
            return self._state[location]
        except IndexError:
            return 0

    def set_memory_location(self, location: int, value: int):
        """
        Sets the location given to the value

        If the location is un-initilised, extends the state to cover the new range
        values initialised with 0 according to spec
        Args:
            location: location in intcode state to store given value
            value: value to store in given location
        """
        assert location >= 0
        # print(f"Writing to loc {location}")
        if location >= len(self._state):
            # print(f"Pre-expand len {len(self._state)}")
            self._state += [0] * (location - len(self._state) + 1)
            # print(f"Post-expand len {len(self._state)}")
        self._state[location] = value

    def run_computer(self) -> iter:
        """
        Runs through current state

        Yields:
            True if computer requires an input
            Value if has processed an output command
            False if reached a halt (99 op code)

        """
        if self._state is None:
            raise Exception("Set state before running computer")

        while True:
            instruction = str(self.get_memory_location(self._ip))
            opcode = int(instruction[-2:])

            if opcode not in self.valid_opcodes:
                raise Exception(f"Opcode {opcode} not in recognised valid codes")

            params = []  # Parameters are memory locations
            for i in range(0, self.valid_opcodes[opcode]["num_params"]):
                # For each parameter of the opcode
                try:
                    # Extract mode from initial instruction
                    test = -3 - i
                    param_mode = int(instruction[-3 - i])
                    assert param_mode in self.param_modes
                except (IndexError, ValueError):
                    # If not specified, default mode is 0
                    param_mode = 0

                if param_mode == 0:
                    # position mode, the the location index is at the value of the parameter
                    # parameter is found at the IP (current instruction) + parameter number
                    params.append(self.get_memory_location(self._ip + i + 1))
                elif param_mode == 1:
                    # immediate mode, param value is where the IP points to
                    params.append(self._ip + i + 1)
                elif param_mode == 2:
                    # Relative mode - position mode but location is modified by the rel-base
                    params.append(self.get_memory_location(location=self._ip + i + 1) + self._relative_base)
                else:
                    raise RuntimeError(f"Invalid param mode : {param_mode}")

            res = self.valid_opcodes[opcode]["func"](params)
            if res is not None:
                # if calculation returned something then need to pause execution to inform
                return res

    # --- Start of opcode functions --- #
    # All functions take a single argument, a list of parameters they require
    # parameters are asserted they contain the correct number of parameter values for the given opcode (as defined in spec)

    def _addition(self, params: List[int]):
        assert len(params) == self.valid_opcodes[1]["num_params"]
        self.set_memory_location(location=params[2],
                                 value=self.get_memory_location(params[0]) + self.get_memory_location(params[1]))
        self._ip += self.valid_opcodes[1]["steps_forward"]
        return None

    def _multiplication(self, params: List[int]):
        assert len(params) == self.valid_opcodes[2]["num_params"]
        self.set_memory_location(location=params[2],
                                 value=self.get_memory_location(params[0]) * self.get_memory_location(params[1]))
        self._ip += self.valid_opcodes[2]["steps_forward"]
        return None

    def _input(self, params: List[int]):
        assert len(params) == self.valid_opcodes[3]["num_params"]
        if self.next_input is None:
            return True
        self.set_memory_location(params[0], value=self.next_input)
        self.next_input = None
        self._ip += self.valid_opcodes[3]["steps_forward"]
        return None

    def _output(self, params: List[int]):
        assert len(params) == 1
        output_val = self.get_memory_location(params[0])
        self._ip += self.valid_opcodes[4]["steps_forward"]
        return output_val

    def _jump_if_true(self, params: List[int]):
        assert len(params) == 2
        if self.get_memory_location(location=params[0]) != 0:
            self._ip = self.get_memory_location(location=params[1])
            return None
        else:
            self._ip += self.valid_opcodes[5]["steps_forward"]
            return None

    def _jump_if_false(self, params: List[int]):
        assert len(params) == 2
        if self.get_memory_location(location=params[0]) == 0:
            self._ip = self.get_memory_location(location=params[1])
            return None
        else:
            self._ip += self.valid_opcodes[6]["steps_forward"]
            return None

    def _less_than(self, params: List[int]):
        assert len(params) == 3
        if self.get_memory_location(params[0]) < self.get_memory_location(params[1]):
            self.set_memory_location(location=params[2], value=1)
        else:
            self.set_memory_location(location=params[2], value=0)
        self._ip += self.valid_opcodes[7]["steps_forward"]
        return None

    def _equals(self, params: List[int]):
        assert len(params) == 3
        if self.get_memory_location(params[0]) == self.get_memory_location(params[1]):
            self.set_memory_location(location=params[2], value=1)
        else:
            self.set_memory_location(location=params[2], value=0)
        self._ip += self.valid_opcodes[8]["steps_forward"]
        return None

    def _relative_base_offset(self, params: List[int]):
        assert len(params) == 1
        self._relative_base += self.get_memory_location(params[0])
        self._ip += self.valid_opcodes[9]["steps_forward"]
        return None

    @staticmethod
    def _end(params: List):
        assert len(params) == 0
        return False
