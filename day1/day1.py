input = "input.txt"
# input = "test1.txt"

def fuel_requirement(mass):
    return int(mass / 3) - 2


total_fuel = 0
with open(input) as input:
    for module_mass in input:
        module_mass = int(module_mass)

        total_module_fuel = fuel_requirement(module_mass)
        print(f"initial fuel is {total_module_fuel}")

        extra_fuel = fuel_requirement(total_module_fuel)
        print(f"Initial fuel req: {extra_fuel}")

        while fuel_requirement(extra_fuel) > 0:
            total_module_fuel += extra_fuel
            extra_fuel = fuel_requirement(extra_fuel)
            print(f"extra fuel required for last fuel is {extra_fuel}")

        total_fuel += extra_fuel

        total_fuel += total_module_fuel

print(total_fuel)
