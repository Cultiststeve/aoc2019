import time
import tkinter

from intcode_computer.intcode_computer import IntcodeComputer

input_path = "input.txt"
with open(input_path) as input_file:
    input_string = input_file.read()
    intcode_program_list = [int(x) for x in input_string.split(sep=',')]

class PaintingRobot:
    def __init__(self):
        self.computer = IntcodeComputer()
        self.facing = 0  # In degrees
        self.x = 0
        self.y = 0

    def move_foward_one(self):
        self.facing = self.facing % 360
        assert self.facing in [0, 90, 180, 270]
        if self.facing == 0:
            self.y += 1  # up
        elif self.facing == 90:
            self.x += 1  # right
        elif self.facing == 180:
            self.y -= 1  # down
        elif self.facing == 270:
            self.x -= 1  # left




def draw_ship_hull(ship_hull, tkinter_root):
    max_x = 0
    max_y = 0
    for panel in ship_hull:
        max_x = max(abs(panel[0]), max_x)
        max_y = max(abs(panel[1]), max_y)

    for panel in ship_hull:
        if ship_hull[panel] == 1:
            color = "white"
        else:
            color = "black"
        tkinter.Button(tkinter_root, bg=color).grid(row=int(panel[0]+max_x),
                                          column=int(panel[1]+max_y))

    tkinter_root.update_idletasks()
    tkinter_root.update()


my_robot = PaintingRobot()
my_robot.computer.set_state(intcode_program_list)

ship_hull = {}
ship_hull[(0,0)] = 1  # Part 2
panels_painted = 0
root_window = tkinter.Tk()

while True:
    # draw_ship_hull(ship_hull, root_window)
    res = my_robot.computer.run_computer()
    if res is False:
        break
    elif res is True:
        if (my_robot.x, my_robot.y) in ship_hull:
            my_robot.computer.next_input = ship_hull[(my_robot.x, my_robot.y)]
        else:
            my_robot.computer.next_input = 0  # assume black
    else:
        # Output a color to paint
        assert res in [0, 1]
        if (my_robot.x, my_robot.y) not in ship_hull.keys():
            panels_painted += 1
        ship_hull[(my_robot.x, my_robot.y)] = res  # paints with 0 or 1
        direction = my_robot.computer.run_computer()
        assert direction in [0, 1]
        if direction == 0:
            my_robot.facing -= 90  # left
        else:
            my_robot.facing += 90  # right
        my_robot.move_foward_one()
        # draw_ship_hull(ship_hull, root_window)
        # root_window.update_idletasks()
        # root_window.update()
        # time.sleep(1)

print(ship_hull)
print(f"Painted {panels_painted} panels")
print(f"Ships hull has {len(ship_hull)} painted panels")

draw_ship_hull(ship_hull, root_window)

root_window.mainloop()
