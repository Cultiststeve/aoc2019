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

    Args:
        x:
        y:
        type: 0 for floor, 1 for wall, 2 for robot
        tkinter_root:

    Returns:

    """
    color = None
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

    tkinter.Button(tkinter_root, bg=color).grid(row=y, column=x, sticky=tkinter.N + tkinter.S + tkinter.E + tkinter.W)
    tkinter_root.update_idletasks()
    tkinter_root.update()

class RemoteRobot:

    def __init__(self):
        self.computer = intcode_computer.IntcodeComputer(initial_state=intcode_program_list)
        self.x = 1000
        self.y = 1000
        self.direction = 0
        self.draw_robot()
        self.known_space = {(self.x, self.y): 1}  # dict of position tuples, value is wall/floor/oyxgen

    def draw_robot(self):
        update_screen(self.x, self.y, 2, root_window)

    def set_random_direction(self):
        self.direction = random.randint(1,4)
        print(f"Set new direction to {self.direction}")

    def set_smart_direction(self):
        if (self.x, self.y+1) not in self.known_space.keys():
            # North
            self.direction = 1
            return
        if (self.x, self.y - 1) not in self.known_space.keys():
            # South
            self.direction = 2
            return
        if (self.x-1, self.y) not in self.known_space.keys():
            # west
            self.direction = 3
            return
        if (self.x+1, self.y) not in self.known_space.keys():
            # east
            self.direction = 4
            return

        best_direction = None
        min_steps_arround = 999
        if self.known_space[(self.x, self.y+1)] < min_steps_arround:
            if self.known_space[(self.x, self.y+1)] >= 0:
                best_direction = 1
                min_steps_arround = self.known_space[(self.x, self.y+1)]
        if self.known_space[(self.x, self.y-1)] < min_steps_arround:
            if self.known_space[(self.x, self.y-1)] >= 0:
                best_direction = 2
                min_steps_arround = self.known_space[(self.x, self.y-1)]
        if self.known_space[(self.x-1, self.y)] < min_steps_arround:
            if self.known_space[(self.x-1, self.y)] >= 0:
                best_direction = 3
                min_steps_arround = self.known_space[(self.x-1, self.y)]
        if self.known_space[(self.x+1, self.y)] < min_steps_arround:
            if self.known_space[(self.x+1, self.y)] >= 0:
                best_direction = 4
                min_steps_arround = self.known_space[(self.x+1, self.y)]
        if best_direction:
            self.direction = best_direction
            return
        print(f"Panic, cant find a new direction")

    def update_postion(self, oxygen=False):
        if oxygen:
            floor_type = 3
        else:
            floor_type = 0
        if self.direction == 1:
            # North
            update_screen(self.x, self.y, floor_type, root_window)
            self.y += 1
            self.draw_robot()
        elif self.direction == 2:
            # South
            update_screen(self.x, self.y, floor_type, root_window)
            self.y -= 1
            self.draw_robot()
        elif self.direction == 3:
            # west
            update_screen(self.x, self.y, floor_type, root_window)
            self.x -= 1
            self.draw_robot()
        elif self.direction == 4:
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

    def wall_in_move_dir(self):
        if self.direction == 1:
            # North
            update_screen(self.x, self.y+1, 1, root_window)
            self.known_space[(self.x, self.y+1)] = -1
        elif self.direction == 2:
            # South
            update_screen(self.x, self.y-1, 1, root_window)
            self.known_space[(self.x, self.y-1)] = -1
        elif self.direction == 3:
            # west
            update_screen(self.x-1, self.y, 1, root_window)
            self.known_space[(self.x-1, self.y)] = -1
        elif self.direction == 4:
            # east
            update_screen(self.x+1, self.y, 1, root_window)
            self.known_space[(self.x+1, self.y)] = -1
        else:
            raise RuntimeError(f"Direction was {self.direction}, not 1-4")



root_window = tkinter.Tk()
robot = RemoteRobot()


while True:
    res = robot.computer.run_computer()
    print(f"robot computer returned {res}")

    if res is True:
        # Computer needs a new direction
        robot.set_smart_direction()
        robot.computer.next_input = robot.direction
    elif res is False:
        # Computer program has exited
        print(f"Computer program has exited")
        break
    else:
        # Must have returned a status code
        assert type(res) is int
        assert 0 <= res <=2

        if res == 1:
            # Robot moved in direction
            robot.update_postion()
        elif res == 0:
            # Hit a wall
            robot.wall_in_move_dir()
        elif res == 2:
            print(f"Found oyxgen place!")
            robot.update_postion(oxygen=True)
            break

root_window.mainloop()