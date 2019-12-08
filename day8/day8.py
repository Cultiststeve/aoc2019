from PIL import Image

input_path = "input.txt"
with open(input_path) as input_file:
    input_string = input_file.read()

# input_string = "123456789012"
print(input_string)

row_len = 25
colum_len = 6
layer_size = row_len*colum_len

layers = []
layer_index = 0
row_index = 0
colum_index = 0

row = []
layer = []
for bit_index in range(0, len(input_string)):


    if ((bit_index-(row_index*row_len)) // row_len) > 0:
        layer.append(row)
        row_index += 1
        row = []

    layer_if = ((bit_index - (layer_index * layer_size)) // layer_size)
    if ((bit_index - (layer_index * layer_size)) // layer_size) > 0:
        layers.append(layer)
        layer_index += 1
        layer = []

    row.append(input_string[bit_index])

layer.append(row)
layers.append(layer)


print(layers)
print(f"There is {len(layers)} layers")
print(f"There should be {len(input_string) / layer_size} layers")

min_0 = 999
for layer in layers:
    print(f"len: {len(layer)}")
    num_0 = 0
    for row in layer:
        print(row)
        num_0 += row.count("0")
    print(f"0's in row is {num_0}")

    if min_0 > num_0:
        min_layer = layer
    min_0 = min(min_0, num_0)

print(f"min is {min_0}")

n1 = 0
n2 = 0
for row in min_layer:
    n1 += row.count("1")
    n2 += row.count("2")

print(f"res : {n1*n2}")

visable = []
# print(visable)
# print("Visible:")
for row in layer:
    vis_row = []
    for bit in row:
        vis_row.append((0,0,0))
    visable.append(vis_row)
    vis_row = []

for layer in layers:
    for ri in range(0, len(layer)):
        for ci in range(0, len(row)):
            if visable[ri][ci] == (0,0,0):
                if layer[ri][ci] == "0":
                    visable[ri][ci] = ((0, 225, 0))
                elif layer[ri][ci] == "1":
                    visable[ri][ci] = ((225, 0, 0))

background =  (0,0,0,255)
image = Image.new("RGBA", (len(visable), len(visable[0])), background)
pixels = image.load()

for row_i in range(0, len(visable)):
    for col_i in range(0, len(row)):
        # print(visable[row_i][col_i])
        pixels[(row_i, col_i)] = visable[row_i][col_i]

image.save("img.png")