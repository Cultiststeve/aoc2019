input_path = "input.txt"
# input_path = "example_1.txt"
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

current_stock = {}  # Dictionary of current products, key is product name, value is quantity
ore_used = 0  # How much ore has been used by product
ore_limit = 1421950879

for chemical in possible_reactions.keys():
    # print(chemical[0])
    current_stock[chemical[0]] = 0


def get_product(product_name, quantity):
    global current_stock
    global ore_used

    # print(f"Get product {product_name} , quantity requested: {quantity}")
    assert product_name in current_stock.keys()

    # Check / get all the reactants for product
    for product_pair in possible_reactions.keys():
        if product_name in product_pair:
            reagents = possible_reactions[product_pair]
            # print(reagents)
            break

    assert reagents is not None

    while current_stock[product_name] < quantity:
        # Do the reaction
        for reagent_pair in reagents:
            if reagent_pair[0] == "ORE":
                if ore_used + reagent_pair[1] > ore_limit:
                    return False  # Stop reacting if reached this
                ore_used += reagent_pair[1]
            else:
                if get_product(reagent_pair[0], quantity=reagent_pair[1]) is False:
                    return False
                current_stock[reagent_pair[0]] -= reagent_pair[1]
        current_stock[product_name] += product_pair[1]
        # print(f"Reaction step done, current stock of {product_name} is now {current_stock[product_name]}")



while get_product('FUEL', current_stock['FUEL']+1) is not False:
    print(f"Produced {current_stock['FUEL']} fuel, using {ore_used} ore")


print(f"Used {ore_used} ore")
print(f"End up with {current_stock} stock")
print(f"Produced {current_stock['FUEL']} fuel")

#1000000000000
