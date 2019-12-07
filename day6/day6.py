input_path = "input.txt"
# input_path = "test2.txt"

with open(input_path) as input_file:
    input_data = input_file.read()

print(input_data)

input_data = input_data.splitlines()

all_objects = {}  # key is of names of objects, with class as value

def min_allow_none(p1, p2):
    if p1 and p2 is not None:
        return min(p1, p2)
    elif p1 is not None:
        return p1
    elif p2 is not None:
        return p2
    else:
        return None

class SpaceObject:
    def __init__(self, name: str, orbits_arround: str):
        self.name = name
        self.orbits_arround = orbits_arround
        self.has_orbiting = []

    def get_orbits(self):
        if self.orbits_arround is None:
            # assert self.name == "COM"  # only COM doesnt orbit
            return 0
        else:
            # has indirect orbits = thing it oribts arround + 1 direct orbit
            return all_objects[self.orbits_arround].get_orbits() + 1

    def distance_to_santa(self, base_route: str):
        """Returns distance to santa, or None if no route"""
        # Are we santa?
        if self.name == "SAN":
            return 0

        min_dist = None
        # Check for object this orbits
        if self.orbits_arround is not None and self.orbits_arround != base_route:
            min_dist = min_allow_none(min_dist, all_objects[self.orbits_arround].distance_to_santa(base_route=self.name))

         # Check objects orbiting arround this
        for obj in self.has_orbiting:
            if all_objects[obj].name != base_route:  # dont check route we came from
                min_dist = min_allow_none(min_dist, all_objects[obj].distance_to_santa(base_route=self.name))

        if min_dist is not None:
            return min_dist + 1
        else:
            return None

    def __str__(self):
        return f"Object name: {self.name}, has orbiters {self.has_orbiting}"


COM_obj = SpaceObject(name="COM", orbits_arround=None)
all_objects["COM"] = COM_obj

for orbit in input_data:
    orbit = orbit.split(sep=')')
    parent_name = orbit[0].strip()
    object_name = orbit[1].strip()

    new_object = SpaceObject(name=object_name, orbits_arround=parent_name)
    all_objects[object_name] = new_object


for orbit in input_data:
    orbit = orbit.split(sep=')')
    parent_name = orbit[0].strip()
    object_name = orbit[1].strip()

    all_objects[parent_name].has_orbiting.append(object_name)


total_orbits = 0
for item in all_objects.values():
    total_orbits += item.get_orbits()
    print(item)
    # if item.name != "COM":
    #     assert item.orbits_arround is not None

# print(indirect_orbits)
print(f"Total orbits = {total_orbits}")

dist_to_santa = all_objects["YOU"].distance_to_santa(base_route="") - 2  # Dont count YOU and SAN's  orbits
print(f"Dist to santa: {dist_to_santa}")