import hashlib
from functools import lru_cache

class Moon:
    def __init__(self, x, y, z, name):
        self.position = [x, y, z]
        self.velocity = [0, 0, 0]
        self.name = name
        self.hash_obj = hashlib.md5()

    @lru_cache(maxsize=None)
    def kinetic(self):
        ke = 0
        for axis in range(0,3):
            ke += abs(self.velocity[axis])
        return ke

    @lru_cache(maxsize=None)
    def potential(self):
        pe = 0
        for axis in range(0, 3):
            pe += abs(self.position[axis])
        return pe

    @lru_cache(maxsize=None)
    def total_energy(self):
        return self.potential() * self.kinetic()

    def state_hash(self):
        self.hash_obj.update(str(self.position).encode())
        self.hash_obj.update(str(self.velocity).encode())
        # self.hash_obj.update(str(self.name).encode())
        return self.hash_obj.digest()


def get_universe_hash(moons):
    moon_hashes = []
    for moon in moons:
        moon_hashes.append(moon.state_hash())

    # print(moon_hashes)
    uni_hash = hashlib.md5(str(moon_hashes).encode()).digest()
    # print(f"Uni hash: {uni_hash}")
    return uni_hash


# <x=-8, y=-18, z=6>
# <x=-11, y=-14, z=4>
# <x=8, y=-3, z=-10>
# <x=-2, y=-16, z=1>

# --- Puzzle Input ---
Io = Moon(-8,-18,6, "Io")
Europa = Moon(-11,-14,4, "Europa")
Ganymede = Moon(8,-3,-10, "Ganymede")
Callisto = Moon(-2,-16,1, "Callisto")

# --- Sample Input ---
Io = Moon(-1, 0, 2, "Io")
Europa = Moon(2, -10, -7, "Europa")
Ganymede = Moon(4, -8, 8, "Ganymede")
Callisto = Moon(3, 5, -1, "Callisto")

# --- Second Example ---
# Io = Moon(-8, -10, 0, "Io")
# Europa = Moon(5, 5, 10, "Europa")
# Ganymede = Moon(2, -7, 3, "Ganymede")
# Callisto = Moon(9, -8, -3, "Callisto")


Moons = [Io, Europa, Ganymede, Callisto]
timesteps = 0
universe_states = set()
universe_states.add(get_universe_hash(Moons))

# 4,686,774,924

while True:
    if (timesteps % 10000) == 0:
        print(f"On timestep {timesteps:,}")
    # Update velocities by applying gravity, only once for each pair
    for current_moon in Moons:
        for affecting_moon in Moons:
            # Dont affect self
            if current_moon is affecting_moon:
                continue

            # for each axis, update velocities
            for axis in range(0, 3):
                if affecting_moon.position[axis] > current_moon.position[axis]:
                    current_moon.velocity[axis] += 1
                elif affecting_moon.position[axis] < current_moon.position[axis]:
                    current_moon.velocity[axis] -= 1
                # no change if equal

    # Apply velocity
    for current_moon in Moons:
        for axis in range(0, 3):
            current_moon.position[axis] += current_moon.velocity[axis]

    timesteps += 1

    # Are we in previous state
    curr_hash = get_universe_hash(Moons)

    if curr_hash in universe_states:
        print(f"Universe has reached a previous state on step {timesteps} with hash {curr_hash}")
        break
    else:
        universe_states.add(curr_hash)

    # if timesteps == 2772:
    #     print(f"Reached max steps...")
    #     break

# Print final state
for current_moon in Moons:
    print(current_moon.position)
    print(f"Kinetic: {current_moon.kinetic()}")
    print(f"Potential: {current_moon.potential()}")
    print(f"Total: {current_moon.total_energy()}")

print(f"Total ke = {sum(moon.total_energy() for moon in Moons)}")

# 51374, low
# 61374 low