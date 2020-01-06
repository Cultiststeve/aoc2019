import time
import tkinter

from intcode_computer import intcode_computer


def update_screen(x, y, type, tkinter_root):
    print(f"updating screen.., x={x}, y={y}")

    color = "black"
    btn_text = tkinter.StringVar()
    if type == 0:
        # empty
        pass
    elif type == 1:
        # wall
        color = "red"
        btn_text.set(x)
    elif type == 2:
        # block
        color = "blue"
    elif type == 3:
        # paddle
        color = "green"
    elif type == 4:
        # ball
        color = "white"

    if y == 0:
        tkinter.Button(tkinter_root, bg=color, textvariable=btn_text).grid(row=y, column=x)
    else:
        tkinter.Button(tkinter_root, bg=color).grid(row=y, column=x, sticky=tkinter.N  + tkinter.S + tkinter.E + tkinter.W)

    tkinter_root.update_idletasks()
    tkinter_root.update()


input_path = "input.txt"
with open(input_path) as input_file:
    input_string = input_file.read()
    intcode_program_list = [int(x) for x in input_string.split(sep=',')]

intcode_program_list[0] = 2  # Part 2
computer = intcode_computer.IntcodeComputer(initial_state=intcode_program_list)

root_window = tkinter.Tk()

res = True
output = []
curr_step_of_program = 0
initial_display = False
joystick_direction = 0  # left is -1, right is 1
paddle_curr_x = -1
ball_curr_x = -1
while res is not False:  # Run game

    res = computer.run_computer()
    if res is True:
        # print("Needs input...")
        computer.next_input = joystick_direction
        continue
    output.append(res)

    if (curr_step_of_program + 1) % 3 == 0:
        x = output[curr_step_of_program - 2]
        y = output[curr_step_of_program - 1]
        block_type = output[curr_step_of_program]
        assert type(x) is int
        assert type(y) is int
        assert type(block_type) is int

        if x < 0:
            assert x == -1
            assert y == 0
            # Score
            print(f"Current score is {block_type}")
            initial_display = True
        else:
            # Dont update screen for a score display
            # update_screen(x, y, block_type, tkinter_root=root_window)
            # if initial_display:  # Once we have done initial draw, slow down game
                # time.sleep(.05)

            if block_type == 3:
                # paddle
                paddle_curr_x = x
            if block_type == 4:
                # Ball
                ball_curr_x = x

            # Check joystick pos
            if ball_curr_x > paddle_curr_x:
                joystick_direction = 1
            elif ball_curr_x == paddle_curr_x:
                joystick_direction = 0
            elif ball_curr_x < paddle_curr_x:
                joystick_direction = -1
            else:
                raise Exception("Cant match ball and paddle curry")

    curr_step_of_program += 1

# print(output)
#
# total_blocks = 0
# for i in range(2, len(output), 3):
#     # print(output[i])
#     if output[i] == 2:
#         total_blocks += 1
#
# print(f"Total blocks: {total_blocks}")
