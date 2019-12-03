# input_path = "test1.txt"
# input_path = "test2.txt"
input_path = "input.txt"

with open(input_path) as input_file:
    wire_one_route = input_file.readline().strip("\n")
    wire_two_route = input_file.readline().strip("\n")

wire_one_route = wire_one_route.split(sep=',')
wire_two_route = wire_two_route.split(sep=',')

print(f"1: {wire_one_route}")
print(f"2: {wire_two_route}")


def manhat_dist(x, y):
    return abs(x) + abs(y)


def get_path(route):
    # print("get path")
    x = 0
    y = 0
    l = 0
    wire_path = {(x, y): l}
    for vector in route:
        dir = vector[0]
        dist = int(vector[1:])
        # print(dir, len)
        for cord in range(0, dist):
            l += 1
            if dir == "R":
                x += 1
            elif dir == "L":
                x -= 1
            elif dir == "U":
                y += 1
            elif dir == "D":
                y -= 1
            else:
                raise Exception(f"Unrecognised direction : {dir}")
            if (x, y) not in wire_path:
                wire_path[(x, y)] = l
    return wire_path


wire_one_path = get_path(wire_one_route)
wire_two_path = get_path(wire_two_route)
print(wire_one_path)
print(wire_two_path)

crossings = (wire_one_path.keys() & (wire_two_path.keys()))
# print(crossings)
print(f"{len(crossings)} crossings")

min_dist = None
for intersect in crossings:
    dist = manhat_dist(intersect[0], intersect[1])
    if min_dist:
        if dist < min_dist:
            min_dist = dist
    else:
        min_dist = dist
print(f"Min dist: {min_dist}")


min_sig_delay = None
for intersect in crossings:
    sig_delay = wire_one_path.get(intersect) + wire_two_path.get(intersect)
    if min_sig_delay:
        if sig_delay < min_sig_delay:
            min_sig_delay = sig_delay
    else:
        min_sig_delay = sig_delay
print(f"Min sig delay: {min_sig_delay}")

