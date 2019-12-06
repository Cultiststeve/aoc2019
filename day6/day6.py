input_path = "input.txt"
# input_path = "test1.txt"

with open(input_path) as input_file:
    input_data = input_file.read()

print(input_data)

input_data = input_data.splitlines()

all_objects = {}  # key is of names of objects, with class as value


class SpaceObject:
    def __init__(self, name: str, orbits_arround: str):
        self.name = name
        self.orbits_arround = orbits_arround

        self.has_orbiting = []

    def get_orbits(self):
        if self.orbits_arround is None:
            assert self.name == "COM"  # only COM doesnt orbit
            return 0
        else:
            # has indirect orbits = thing it oribts arround + 1 direct orbit
            return all_objects[self.orbits_arround].get_orbits() + 1

    def __str__(self):
        return f"Object name: {self.name}, has orbiters {self.has_orbiting}"

COM_obj = SpaceObject(name="COM", orbits_arround=None)
all_objects["COM"] = COM_obj

for orbit in input_data:
    orbit = orbit.split(sep=')')
    parent_name = orbit[0].strip()
    object_name = orbit[1].strip()

    if parent_name not in all_objects.keys():
        parent_object = SpaceObject(name=parent_name, orbits_arround=None)
        all_objects[parent_name] = parent_object
        # is replaced by below process when encountered later in list

    new_object = SpaceObject(name=object_name, orbits_arround=parent_name)
    all_objects[object_name] = new_object
    all_objects[parent_name].has_orbiting.append(object_name)

total_orbits = 0
for item in all_objects.values():
    total_orbits += item.get_orbits()
    print(item)

# print(indirect_orbits)
print(f"Total orbits = {total_orbits}")
