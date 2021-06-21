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

    computer = Computer(INSTRUCTIONS)
    assert computer.get_accumulator_after_stop()[1] == 1797

    assert get_accumulator_after_fixing_program(INSTRUCTIONS) == 1036

def test_challenge9():
    from challenge9 import NUMBERS, find_first_wrong_number, find_encryption_weakness

    assert find_first_wrong_number(NUMBERS) == 21806024

    assert find_encryption_weakness(NUMBERS) == 2986195

def test_challenge10():
    from challenge10 import ADAPTERS, find_all_ways_to_arrange_adapters, get_joltage_product

    assert get_joltage_product(ADAPTERS) == 1820

    assert find_all_ways_to_arrange_adapters(ADAPTERS) == 3454189699072


# skipping 11 - it takes too long


def test_challenge12():
    from challenge12 import MOVES, get_manhattan_distance_after_waypoint_moves, get_manhattan_distance_after_travelling

    assert get_manhattan_distance_after_travelling(MOVES) == 2847
    assert get_manhattan_distance_after_waypoint_moves(MOVES) == 29839

def test_challenge13():
    from challenge13 import TIMESTAMP, BUS_IDS, find_timestamp_for_consecutive_busses, get_first_bus_after_timestamp

    assert get_first_bus_after_timestamp(TIMESTAMP, BUS_IDS) == 2045
    assert find_timestamp_for_consecutive_busses(BUS_IDS) == 402251700208309

def test_challenge14():
    from challenge14 import INSTRUCTIONS, get_sum_of_memory, get_sum_of_memory_v2

    assert get_sum_of_memory(INSTRUCTIONS) == 11612740949946

    assert get_sum_of_memory_v2(INSTRUCTIONS) == 3394509207186

def test_challenge15():
    from challenge15 import PREAMBLE, get_nth_word_spoken

    assert get_nth_word_spoken(PREAMBLE, 10 == 273)
    assert get_nth_word_spoken(PREAMBLE, 300000 == 47205)

def test_challenge16():
    from challenge16 import TICKET_DATA

    assert TICKET_DATA.get_ticket_scanning_error_rate() == 25984
    assert TICKET_DATA.get_departure_fields_product() == 1265347500049

def test_challenge17():
    from challenge17 import STARTING_DATA, get_active_squares_after_n_cycles

    assert get_active_squares_after_n_cycles(STARTING_DATA, 6) == 359

def test_challenge18():
    from challenge18 import EQUATIONS, get_sum_of_equations

    assert get_sum_of_equations(EQUATIONS) == 8298263963837
    assert get_sum_of_equations(EQUATIONS, True) == 145575710203332

def test_challenge19():
    from challenge19 import MESSAGE_DATA_WITH_SUBSTITUTIONS, MESSAGE_DATA
    assert MESSAGE_DATA.get_number_of_matching_rules("0") == 241
    assert MESSAGE_DATA_WITH_SUBSTITUTIONS.get_number_of_matching_rules("0") == 424

def test_challenge20():
    from challenge20 import ASSEMBLED_TILES, get_corners_multiplied, get_non_sea_monsters
    assert get_corners_multiplied(ASSEMBLED_TILES) == 111936085519519
    assert get_non_sea_monsters(ASSEMBLED_TILES) == 1792

def test_challenge21():
    from challenge21 import MEALS, get_number_of_times_nonallergen_ingredients_appear, get_canonically_dangerous_ingredient

    assert get_number_of_times_nonallergen_ingredients_appear(MEALS) == 2203
    assert get_canonically_dangerous_ingredient(MEALS) == 'fqfm,kxjttzg,ldm,mnzbc,zjmdst,ndvrq,fkjmz,kjkrm'
