def test_challenge1():
    from challenge1 import ENTRIES, get_entries_summing_to
    assert get_entries_summing_to(ENTRIES, 2020) == (438, 1582)

    assert get_entries_summing_to(ENTRIES, 2020, 3) == (688, 514, 818)

def test_challenge2():
    from challenge2 import PASSWORDS, get_number_of_valid_passwords, get_number_of_old_valid_passwords
    assert get_number_of_old_valid_passwords(PASSWORDS) == 410
    
    assert get_number_of_valid_passwords(PASSWORDS) == 694

def test_challenge3():
    from challenge3 import TREE_GRID, get_number_of_trees_hit

    assert get_number_of_trees_hit(TREE_GRID, 3) == 265

def test_challenge4():
    from challenge4 import PASSPORTS, get_number_of_valid_passports, get_number_of_valid_data_passports

    assert get_number_of_valid_passports(PASSPORTS) == 222

    assert get_number_of_valid_data_passports(PASSPORTS) == 140

def test_challenge5():
    from challenge5 import BOARDING_PASSES, get_highest_seat_id, find_seat_id

    assert get_highest_seat_id(BOARDING_PASSES) == 976

    assert find_seat_id(BOARDING_PASSES) == 685

def test_challenge6():
    from challenge6 import QUESTIONS, get_sum_of_all_yes_counts, get_sum_of_any_yes_counts

    assert get_sum_of_any_yes_counts(QUESTIONS) == 6506

    assert get_sum_of_all_yes_counts(QUESTIONS) == 3243

def test_challenge7():
    from challenge7 import BAG_RULES, get_number_of_bags_able_to_hold_bag, get_number_of_bags_inside

    assert get_number_of_bags_able_to_hold_bag(BAG_RULES, "shiny gold") == 302
    assert get_number_of_bags_inside(BAG_RULES, "shiny gold") == 4165

def test_challenge8():
    from challenge8 import INSTRUCTIONS, Computer, get_accumulator_after_fixing_program

    computer = Computer(instructions)
    assert computer.get_accumulator_after_stop(INSTRUCTIONS) == 1797

    assert get_accumulator_after_fixing_program(INSTRUCTIONS == 1036)
