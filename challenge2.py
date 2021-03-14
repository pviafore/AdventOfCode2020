from dataclasses import dataclass

import common.input_data as input_data


@dataclass
class Policy:
    min_val: int
    max_val: int
    letter: str

@dataclass
class Password:
    policy: Policy
    password: str

    def is_valid_old(self):
        return (self.policy.min_val <=
                    self.password.count(self.policy.letter)
                <= self.policy.max_val)

    def is_valid(self):
        min_index = self.policy.min_val - 1
        max_index = self.policy.max_val - 1
        return ((self.password[min_index] == self.policy.letter) ^
                (self.password[max_index] == self.policy.letter))


def to_password(text: str) -> Password:
    value_range, letter, password = text.split(" ")
    min_val, max_val = value_range.split("-")
    return Password(
        Policy(int(min_val), int(max_val), letter[0]),
        password
    )

def get_number_of_old_valid_passwords(passwords: list[Password]) -> int:
    return len([p for p in passwords if p.is_valid_old()])

def get_number_of_valid_passwords(passwords: list[Password]) -> int:
    return len([p for p in passwords if p.is_valid()])

PASSWORDS = input_data.read("input/input2.txt", to_password)

if __name__ == "__main__":
    print("The number of old valid passwords is "
          f"{get_number_of_old_valid_passwords(PASSWORDS)}")

    print("The number of old valid passwords is "
          f"{get_number_of_valid_passwords(PASSWORDS)}")
