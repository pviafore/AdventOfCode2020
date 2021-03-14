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
