import math
import random
import time
import tkinter

from intcode_computer import intcode_computer

input_path = "input.txt"
with open(input_path) as input_file:
    input_string = input_file.read()
    intcode_program_list = [int(x) for x in input_string.split(sep=',')]

def update_screen(x, y, type, tkinter_root):
    """
    Draw a box on the grid
    Args:
        x:
        y:
        type: 0 for floor, 1 for wall, 2 for robot
        tkinter_root:

    Returns:

    """
    color = None
    btn_text = tkinter.StringVar()
    btn_text.set(f"({x},{y})")
    if type == 0:
        # empty
        color = "white"
    elif type == 1:
        # wall
        color = "black"
    elif type == 2:
        # robot
        color = "red"
    elif type == 3:
        color == "blue"

    tkinter.Button(tkinter_root, bg=color, textvariable=btn_text).grid(row=y, column=x, sticky=tkinter.N + tkinter.S + tkinter.E + tkinter.W)
    tkinter_root.update_idletasks()
    tkinter_root.update()

class Robot:

    def __init__(self):
        self.computer = intcode_computer.IntcodeComputer(initial_state=intcode_program_list)
        # offset from 0 for easy tkinter drawing
        self.x = 5000
        self.y = 5000
        self.last_direction_attempted = None
        self.current_on_oxygen = False
        self.known_space = {(self.x, self.y): 1}  # dict of position tuples, value is wall/floor/oyxgen
        self.current_path = [(self.x, self.y)]


    def draw_robot(self):
        update_screen(self.x, self.y, 2, root_window)

    def get_next_direction(self):
        # If there is an unknown space, go there
        direction = -1
        # self.draw_robot()
        while direction == -1:
            if (self.x, self.y + 1) not in self.known_space.keys():
                # North
                direction = 1
            elif (self.x, self.y - 1) not in self.known_space.keys():
                # South
                direction = 2
            elif (self.x - 1, self.y) not in self.known_space.keys():
                # west
                direction = 3
            elif (self.x + 1, self.y) not in self.known_space.keys():
                # east
                direction = 4
            else:
                # Backtrack
                if len(self.current_path) == 0:
                    return False
                last_space = self.current_path.pop()
                self.x = last_space[0]
                self.y = last_space[1]
                self.last_direction_attempted = -1
                print(f"Backtracking to {self.x}, {self.y}")

        print(f"Set new direction to {direction}")
        self.last_direction_attempted = direction
        return direction

    def successfull_move(self, found_oxygen=False):
        assert self.last_direction_attempted in range(1,5)
        if self.current_on_oxygen:  # If we are standing on oxygen
            floor_type = 3
        else:
            floor_type = 0
        if self.last_direction_attempted == 1:
            # North
            update_screen(self.x, self.y, floor_type, root_window)
            self.y += 1
            self.draw_robot()
        elif self.last_direction_attempted == 2:
            # South
            update_screen(self.x, self.y, floor_type, root_window)
            self.y -= 1
            self.draw_robot()
        elif self.last_direction_attempted == 3:
            # west
            update_screen(self.x, self.y, floor_type, root_window)
            self.x -= 1
            self.draw_robot()
        elif self.last_direction_attempted == 4:
            # east
            update_screen(self.x, self.y, floor_type, root_window)
            self.x += 1
            self.draw_robot()
        else:
            raise RuntimeError(f"Direction was {self.direction}, not 1-4")
        if (self.x, self.y) in self.known_space.keys():
            self.known_space[(self.x, self.y)] += 1
        else:
            self.known_space[(self.x, self.y)] = 1
        self.current_path.append((self.x, self.y))

        if found_oxygen:
            self.current_on_oxygen = True
            print(f"Found oyxgen at {self.x}, {self.y} with a path length of {len(self.current_path)}")
        else:
            self.current_on_oxygen = False

    def wall_in_move_dir(self):
        assert self.last_direction_attempted in range(1,5)
        if self.last_direction_attempted == 1:
            # North
            self.known_space[(self.x, self.y + 1)] = -1
            update_screen(self.x, self.y + 1, 1, root_window)
        elif self.last_direction_attempted == 2:
            # South
            self.known_space[(self.x, self.y - 1)] = -1
            update_screen(self.x, self.y - 1, 1, root_window)
        elif self.last_direction_attempted == 3:
            # west
            self.known_space[(self.x - 1, self.y)] = -1
            update_screen(self.x - 1, self.y, 1, root_window)
        elif self.last_direction_attempted == 4:
            # east
            self.known_space[(self.x + 1, self.y)] = -1
            update_screen(self.x + 1, self.y, 1, root_window)
        else:
            raise RuntimeError(f"Direction was {self.last_direction_attempted}, not 1-4")

root_window = tkinter.Tk()
my_robot = Robot()

while True:
    res = my_robot.computer.run_computer()
    # print(f"Computer returned {res}")

    if res is True:
        # Computer needs a new direction
        my_robot.computer.next_input = my_robot.get_next_direction()
        time.sleep(.1)
        if my_robot.computer.next_input is False:
            break
    elif res is False:
        # Computer program has exited
        print(f"Computer program has exited")
        break
    else:
        # Must have returned a status code
        assert type(res) is int
        assert 0 <= res <= 2

        if res == 1:
            # Robot moved in direction
            my_robot.successfull_move()
        elif res == 0:
            # Hit a wall
            my_robot.wall_in_move_dir()
        elif res == 2:
            print(f"Found oyxgen at {my_robot.x}, {my_robot.y}!")
            my_robot.successfull_move(oxygen=True)

print(f"Robot has finished mapping.")
root_window.mainloop()
