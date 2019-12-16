import math

input_path = "input.txt"
input_path = "test1.txt"
input_path = "test3.txt"
asteroid_grid = []  # List of rows
asteroid_positions = set()
with open(input_path) as input_file:
    grid_len_x = len(input_file.readline().strip())


with open(input_path) as input_file:
    num_lines = 0
    for _ in input_file:
        num_lines+=1
    grid_len_y = num_lines

print(f"Grid x len  is {grid_len_x}")
print(f"Grid y len  is {grid_len_y}")

with open(input_path) as input_file:
    # y = grid_len - 1
    y = 0
    for line in input_file:
        x = 0
        asteroid_row = []
        for pos in line.strip():
            asteroid_row.append(pos)
            if pos == '#':
                asteroid_positions.add((x, y))
            x += 1
        asteroid_grid.append(asteroid_row)
        y += 1

# print(f"Grid is xlen {len(asteroid_grid[0])}, y-height {len(asteroid_grid)}")

print(f"Roid positions: {asteroid_positions}")

asteroid_visible_count = {}
for roid in asteroid_positions:
    can_see = 0
    for target_roid in asteroid_positions:
        if roid == target_roid:
            continue
        blocked = False
        x_diff = abs(roid[0] - target_roid[0])
        y_diff = abs(roid[1] - target_roid[1])
        # print(f"x {x_diff}, y {y_diff}")

        if x_diff == 0:
            # On same plane
            x = roid[0]
            for y in range(min(roid[1], target_roid[1]) + 1,
                           max(roid[1], target_roid[1])):
                if (x, y) in asteroid_positions:
                    blocked = True
                    break
        elif y_diff == 0:
            # On same plane
            y = roid[1]
            for x in range(min(roid[0], target_roid[0]) + 1,
                           max(roid[0], target_roid[0])):
                if (x, y) in asteroid_positions:
                    blocked = True
                    break
        else:
            angle_between = math.atan((target_roid[1] - roid[1]) / (target_roid[0] - roid[0]))
            # print(f"Angle between: {math.degrees(angle_between)}")

            for x in range(min(roid[0], target_roid[0]) + 1,
                           max(roid[0], target_roid[0])):
                for y in range(min(roid[1], target_roid[1]) + 1,
                               max(roid[1], target_roid[1])):
                    # print(f"{x}-{y}")
                    look_angle = math.atan((y - roid[1]) / (x - roid[0]))
                    if look_angle == angle_between:
                        # print(f"at {x}-{y} angle matches")
                        if (x, y) in asteroid_positions:
                            blocked = True

        if not blocked:
            can_see += 1
    asteroid_visible_count[roid] = can_see

print(asteroid_visible_count)

# for x in range(0, len(asteroid_visible_count)):
#     count = sum(value == x for value in asteroid_visible_count.values())
#     if count > 0:
#         print(f"Num of {x} is {count}")


for y in range(0, grid_len_y):
    for x in range(0, grid_len_x):
        if (x, y) in asteroid_visible_count:
            print(asteroid_visible_count[x, y], end='')
        else:
            print(".", end='')
    print("\n", end='')


station_pos = max(asteroid_visible_count, key=asteroid_visible_count.get)
print(f"Best station is at {station_pos}, can see {asteroid_visible_count[station_pos]}")

angle_from_station = {}
for roid in asteroid_visible_count:
    if roid == station_pos:
        continue
    xdiff = roid[0] - station_pos[0]
    ydiff = roid[1] - station_pos[1]
    try:
        angle_between = math.atan(abs(ydiff) / abs(xdiff))
        angle_between = math.degrees(angle_between)
    except ZeroDivisionError:
        angle_between = 90


    if xdiff >= 0 and ydiff < 0:
        angle_between = 90-angle_between
    elif xdiff >= 0 and ydiff >= 0:
        angle_between += 90  # bottom right
    elif xdiff < 0 and ydiff >= 0:
        angle_between += 180
    else:
        angle_between += 270

    angle_from_station[roid] = angle_between

print(f"Angles: {angle_from_station}")
for y in range(0, grid_len_y):
    for x in range(0, grid_len_x):
        if (x, y) in angle_from_station.keys():
            print(f"\t{round(angle_from_station[(x,y)])}\t", end='')
        else:
            print('\t.\t', end='')
    print("\n", end='')

angles_sorted = list(angle_from_station.values())
angles_sorted.sort()
print(angles_sorted)
asteroid_angles_left = angles_sorted.copy()


asteroids_left = angle_from_station.copy()

def draw_astroid_dict(positions):
    global station_pos
    for y in range(0, grid_len_y):
        for x in range(0, grid_len_x):
            if (x,y) in positions.keys():
                print('#', end='')
            elif (x,y) == station_pos:
                print('X', end='')
            else:
                print('.', end='')
        print("\n", end='')

draw_astroid_dict(asteroids_left)

# Sweep laser through angles
print("\n\n---- Starting laser sweep -----\n\n")
rotation = 0
while len(asteroid_angles_left) > 0:
    print(f"On rotation {rotation}, {len(asteroid_angles_left)} angles left")

    last_angle = -1
    to_remove = []
    for angle in asteroid_angles_left:
        if last_angle == angle:
            continue  # Laser only hits 1 angle on each rotation
        num_roid_at_angle = asteroid_angles_left.count(angle)
        print(f"{num_roid_at_angle} asteroids at angle {angle}")

        asteroids_at_angle = []
        for roid in asteroids_left:
            if asteroids_left[roid] == angle:
                asteroids_at_angle.append(roid)

        closest_postion = None
        min_dist = None
        for roid in asteroids_at_angle:
            xdiff = roid[0] - station_pos[0]
            ydiff = roid[1] - station_pos[1]
            distance_from_station = math.sqrt(xdiff*xdiff + ydiff*ydiff)
            print(f"{roid} is {distance_from_station} from station")
            if min_dist is None:
                min_dist = distance_from_station
                closest_postion = roid
            else:
                min_dist = min(min_dist, distance_from_station)
            closest_postion = roid
            print(f"At angle {angle}, astroids at postions {asteroids_left}")

        asteroids_left.pop(closest_postion)
        draw_astroid_dict(asteroids_left)
        to_remove.append(angle)
        last_angle = angle

    rotation += 1
    for angle in to_remove:
        asteroid_angles_left.remove(angle)

