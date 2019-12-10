import pytest

from intcode_computer.intcode_computer import IntcodeComputer


def test_day_3_prog_1():
    test_prog = [1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50]
    ic = IntcodeComputer(initial_state=test_prog)
    res = True
    output = []
    while res is not False:
        res = ic.run_computer()
        # print(res)
        output.append(res)
    assert res is False  # End of program
    test_prog_final = test_prog.copy()
    test_prog_final[0] = 3500
    test_prog_final[3] = 70
    assert len(output[:-1]) == 0
    assert ic._state == test_prog_final


def test_day_3_prog_5():
    test_prog = [1, 1, 1, 4, 99, 5, 6, 0, 99]
    ic = IntcodeComputer(initial_state=test_prog)
    res = True
    output = []
    while res is not False:
        res = ic.run_computer()
        # print(res)
        output.append(res)
    assert res is False  # End of program
    assert len(output[:-1]) == 0
    test_prog_final = [30, 1, 1, 4, 2, 5, 6, 0, 99]
    assert ic._state == test_prog_final


def test_day_5_prog_1():
    test_prog = [3, 0, 4, 0, 99]
    ic = IntcodeComputer(initial_state=test_prog)
    res = True
    output = []
    my_input = 5
    while res is not False:
        res = ic.run_computer()
        # print(res)
        output.append(res)
        if res is True:
            ic.next_input = my_input
    assert res is False  # End of program
    assert len(output[:-1]) == 2
    assert output[0] is True
    assert output[1] == my_input


def test_day_5_prog_2():
    test_prog = [1002, 4, 3, 4, 33]
    ic = IntcodeComputer(initial_state=test_prog)
    res = True
    output = []
    while res is not False:
        res = ic.run_computer()
        # print(res)
        output.append(res)
    assert res is False  # End of program
    assert len(output[:-1]) == 0
    test_prog_final = [1002, 4, 3, 4, 99]
    assert ic._state == test_prog_final


def test_day_5_equal_to():
    test_prog = [3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8]
    ic = IntcodeComputer(initial_state=test_prog)
    res = True
    output = []
    my_input = 5
    ic.next_input = my_input
    while res is not False:
        res = ic.run_computer()
        # print(res)
        output.append(res)
    assert res is False  # End of program
    assert len(output[:-1]) == 1
    assert output[0] == 0


def test_day_5_jump_pos():
    test_prog = [3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9]
    ic = IntcodeComputer(initial_state=test_prog)
    res = True
    output = []
    while res is not False:
        res = ic.run_computer()
        # print(res)
        output.append(res)
        if res is True:
            ic.next_input = 5
    print(output)

def test_day_9_prog_1():
    test_prog = [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99]
    ic = IntcodeComputer(initial_state=test_prog)
    res = True
    output = []
    while res is not False:
        res = ic.run_computer()
        # print(res)
        output.append(res)
    assert res is False  # End of program
    assert output[:-1] == test_prog  # test prog 1 prints itself


def test_day_9_prog_2():
    test_prog = [1102, 34915192, 34915192, 7, 4, 7, 99, 0]
    ic = IntcodeComputer(initial_state=test_prog)
    res = True
    output = []
    while res is not False:
        res = ic.run_computer()
        # print(res)
        output.append(res)
    assert res is False  # End of program
    assert len(str(output[0])) == 16  # test prog 2 prints a 16 char


def test_day_9_prog_3():
    test_prog = [104, 1125899906842624, 99]
    ic = IntcodeComputer(initial_state=test_prog)
    res = True
    output = []
    while res is not False:
        res = ic.run_computer()
        # print(res)
        output.append(res)
    assert res is False  # End of program
    assert output[0] == test_prog[1]  # test prog 2 prints a 16 char


def test_boost_program():
    with open("boost.txt") as input_file:
        input_string = input_file.read()
        boost_program = [int(x) for x in input_string.split(sep=',')]
    ic = IntcodeComputer(initial_state=boost_program)
    ic.next_input = 1
    res = True
    output = []
    while res is not False:
        res = ic.run_computer()
        # print(res)
        output.append(res)
    assert res is False  # End of program
    print(output)
    assert len(output[:-1]) == 1  # Boost should only produce a single integer
    my_correct_res = 3518157894  # for my input, this is what boost should output (when input 1)
    assert output[0] == my_correct_res
