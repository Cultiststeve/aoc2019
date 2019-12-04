input_lower = 109165
input_upper = 576723

possible_values = 0
for test in range(input_lower, input_upper):
    incrementing = True
    two_ajacent = False
    test_str = str(test)
    for digit_index in range(0, len(test_str)):
        if digit_index > 0:
            # test for ajacent
            if test_str[digit_index] == test_str[digit_index-1]:
                two_ajacent = True

            # test for incresing only
            if test_str[digit_index] < test_str[digit_index-1]:
                incrementing = False
                break

    if incrementing and two_ajacent:
        possible_values += 1
        print(f"{test} is a possible value")

print(f"there is {possible_values} possibles")