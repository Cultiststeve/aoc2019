input_lower = 109165
input_upper = 576723

possible_values = 0
for test in range(input_lower, input_upper):
    incrementing = True
    two_ajacent = False
    test_str = str(test)
    for digit_index in range(1, len(test_str)):
        # test for incresing only
        if test_str[digit_index] < test_str[digit_index-1]:
            incrementing = False
            break

    # This would have been a better way of part 1 also
    # Because the only incrementing rule, if duplicates exist in string they must be ajacent
    for possible_aj_digit in range(0, 10):
        num_digits = test_str.count(str(possible_aj_digit))
        if num_digits == 2:
            two_ajacent = True

    if incrementing and two_ajacent:
        possible_values += 1
        print(f"{test} is a possible value")


print(f"there is {possible_values} possibles")