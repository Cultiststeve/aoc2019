import math

input_path = "input.txt"
input_path = "test1.txt"
input_path = "test2.txt"
asteroid_grid = []  # List of rows
asteroid_positions = set()
with open(input_path) as input_file:
    grid_len = len(input_file.readline().strip())
print(f"Grid len is {grid_len}")

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


for y in range(0, grid_len):
    for x in range(0, grid_len):
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
    xdiff = station_pos[0] - roid[0]
    ydiff = station_pos[1] - roid[1]
    try:
        angle_between = math.atan(ydiff / xdiff)
    except ZeroDivisionError:
        angle_between = 0
    angle_between = math.degrees(angle_between)

    if ydiff < 0:
        angle_between += 270
    elif xdiff and ydiff < 0:
        angle_between += 180
    elif xdiff < 0:
        angle_between += 90

    angle_from_station[roid] = angle_between

print(f"Angles: {angle_from_station}")