import math

input_path = "input.txt"
# input_path = "example_1.txt"
# input_path = "example_2.txt"
# input_path = "example_5.txt"

possible_reactions = {}

with open(input_path) as input_file:
    for line in input_file:
        # print("\n---------\n")
        reaction_string = line.strip()
        # print(reaction_string)
        # print(f"Reaction string split: {reaction_string.split('=')}")
        reactants_str = reaction_string.split('=')[0].strip()
        product_str = reaction_string.split('>')[1].strip()

        # print(product_str)

        product_quantity = int(product_str.strip().split(' ')[0].strip())
        # print(f"Product quantity:  {product_quantity}")
        product = product_str.strip().split(' ')[1].strip()

        # print(f"Reactants: {reactants_str}, produces: {product_quantity} x {product}")

        reactants = reactants_str.split(',')
        # print(f"All Reactants: {reactants}")
        reactant_set = set()
        for reactant_str in reactants:
            reactant_quantity = int(reactant_str.strip().split(' ')[0].strip())
            reactant = reactant_str.strip().split(' ')[1].strip()
            # print(f"Reactant: {reactant}, quantity: {reactant_quantity}")
            reactant_set.add((reactant, reactant_quantity))
        # break

        possible_reactions[(product, product_quantity)] = reactant_set


# Dictonary of reactions
# Key is (product, quantity produced)
# Value is a set of ((reagant, quantity required), (...), ...)
print(possible_reactions)


def do_reaction(product_name, quantity_required, current_stock):
    # print(f"----\nGet product {product_name} , quantity requested: {quantity_required}")

    # Check / get all the reactants for product
    product_pair = None
    reagents = None
    for possible_pair in possible_reactions.keys():
        if product_name in possible_pair:
            reagents = possible_reactions[possible_pair]
            # print(reagents)
            product_pair = possible_pair
            break

    num_product_required = quantity_required - current_stock[product_pair[0]]  # Account for existing stock
    num_reactions = math.ceil(num_product_required / product_pair[1])
    # print(f"Will attempt this reaction {num_reactions} times at once")
    assert num_reactions >= 0
    if num_reactions == 0:
        return current_stock

    for reagent_pair in reagents:
        if reagent_pair[0] == "ORE":
            current_stock['ORE'] += reagent_pair[1]*num_reactions  # Add ore used to stock
        else:
            total_reagent_required = reagent_pair[1]*num_reactions
            new_reagent_required =  total_reagent_required - current_stock[reagent_pair[0]]
            if new_reagent_required > 0:
                # If we require more reagent, do the reaction
                current_stock = do_reaction(reagent_pair[0], total_reagent_required, current_stock)

            current_stock[reagent_pair[0]] -= reagent_pair[1]*num_reactions  # Consume the reagent
            assert current_stock[reagent_pair[0]] >= 0  # Check we havent used more than we had

    current_stock[product_name] += product_pair[1]*num_reactions  # Add the product to the stock

    # print(f"Reaction step done, current stock of {product_name} is now {current_stock[product_name]}")
    return current_stock


initial_stock = {'ORE': 0}  # Dictionary of current products, key is product name, value is quantity
for product_pair in possible_reactions.keys():
    initial_stock[product_pair[0]] = 0

res = do_reaction('FUEL', 1, initial_stock.copy())
print("")
print(f"Final stock: {res}")
print(f"This reaction used {res['ORE']} ore.")


TOTAL_ORE_HELD = 1000000000000
FUEL = 'FUEL'
ORE = 'ORE'

lower_search_bound = 1
upper_search_bound = 1000000000000

found_exact = False
while found_exact is False:
    print(f"New search space between {lower_search_bound} and {upper_search_bound}")
    if lower_search_bound + 1 == upper_search_bound:
        print(f"Lower search bound is same as upper, no more space to look. Closest result is {upper_search_bound}")
        found_exact = True
        break
    search_target_fuel_num = round(((upper_search_bound - lower_search_bound) / 2) + lower_search_bound)
    search_result = do_reaction(FUEL, search_target_fuel_num, initial_stock.copy())
    assert search_result[FUEL] == search_target_fuel_num
    print(f"Search target requires {search_result[ORE]} ore to produce {search_target_fuel_num} fuel")

    if search_result[ORE] > TOTAL_ORE_HELD:
        # If that much fuel would require more ore than we hold
        upper_search_bound = search_target_fuel_num
    elif search_result[ORE] < TOTAL_ORE_HELD:
        # If we used less ore than we hold
        lower_search_bound = search_target_fuel_num
    elif search_result[ORE] == TOTAL_ORE_HELD:
        print(f"Found an exact match with {search_target_fuel_num} fuel produced")
        found_exact = True

print(f"With trillion ore, max fuel that can be produced is {lower_search_bound}")
