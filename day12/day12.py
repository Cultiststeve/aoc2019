class Moon:
    def __init__(self, x, y, z):
        self.position = [x, y, z]
        self.velocity = [0, 0, 0]

    def kinetic(self):
        ke = 0
        for axis in range(0,3):
            ke += abs(self.velocity[axis])
        return ke

    def potential(self):
        pe = 0
        for axis in range(0, 3):
            pe += abs(self.position[axis])
        return pe

    def total_energy(self):
        return self.potential() * self.kinetic()

# <x=-8, y=-18, z=6>
# <x=-11, y=-14, z=4>
# <x=8, y=-3, z=-10>
# <x=-2, y=-16, z=1>

# --- Puzzle Input ---
Io = Moon(-8,-18,6)
Europa = Moon(-11,-14,4)
Ganymede = Moon(8,-3,-10)
Callisto = Moon(-2,-16,1)

# --- Sample Input ---
# Io = Moon(-1, 0, 2)
# Europa = Moon(2, -10, -7)
# Ganymede = Moon(4, -8, 8)
# Callisto = Moon(3, 5, -1)

Moons = [Io, Europa, Ganymede, Callisto]

timesteps = 0
while True:
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
    if timesteps == 1000:
        break

for current_moon in Moons:
    print(current_moon.position)
    print(f"Kinetic: {current_moon.kinetic()}")
    print(f"Potential: {current_moon.potential()}")
    print(f"Total: {current_moon.total_energy()}")

print(f"Total ke = {sum(moon.total_energy() for moon in Moons)}")