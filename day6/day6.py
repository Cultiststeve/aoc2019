input_path = "input.txt"
# input_path = "test1.txt"

with open(input_path) as input_file:
    input_data = input_file.read()


print(input_data)

input_data = input_data.splitlines()

direct_orbits = 0
indirect_orbits = 0


class SpaceObject:
    def __init__(self, name: str, direct_orbit_object):
        self.name = name
        self.direct_orbit_object = direct_orbit_object

        if direct_orbit_object:
            self.is_base = False
            if self.direct_orbit_object.is_base is False:
                self.indirect_orbits = self.direct_orbit_object.indirect_orbits + 1
            else:
                self.indirect_orbits = 0
        else:
            self.is_base = True
            self.indirect_orbits = 0
        print(f"new obj with name {self.name} and {self.indirect_orbits} indirects")

    def get_indirect_orbits(self):
        if self.direct_orbit_object is None:
            return 0
        else:
            return self.direct_orbit_object.get_indirect_orbits() + 1

    def __str__(self):
        return self.name


all_objects = {}  # key is of names of objects, with class as value


for orbit in input_data:
    # print(f"Orbit: {orbit}")
    direct_orbits += 1
    orbit = orbit.split(sep=')')
    parent_name = orbit[0].strip()
    if parent_name not in all_objects.keys():
        new_base_object = SpaceObject(name=parent_name,
                                      direct_orbit_object=None)
        all_objects[parent_name] = new_base_object
    new_name = orbit[1].strip()
    if new_name in all_objects.keys():
        all_objects[new_name].direct_orbit_object = all_objects[parent_name]
    else:
        new_object = SpaceObject(name=new_name,
                                 direct_orbit_object=all_objects[parent_name])
        all_objects[new_object.name] = new_object
    # print(f"all objs: {all_objects}" )


for item in all_objects.values():
    indirect_orbits += item.get_indirect_orbits()

# print(indirect_orbits)
print(f"Total orbits = {indirect_orbits}")

