import itertools
import re
from collections import defaultdict
from dataclasses import dataclass
from typing import Iterable, Optional

import common.input_data as input_data

@dataclass
class Passport: # pylint: disable=R0902
    birth_year: Optional[str]
    issue_year: Optional[str]
    expiration_year: Optional[str]
    height: Optional[str]
    hair_color: Optional[str]
    eye_color: Optional[str]
    passport_id: Optional[str]
    country_id: Optional[str]

    def is_valid(self):
        if self.is_data_valid():
            print(self)
        return (self.birth_year is not None and
                self.issue_year is not None and
                self.expiration_year is not None and
                self.height is not None and
                self.hair_color is not None and
                self.eye_color is not None and
                self.passport_id is not None)

    def is_birth_year_valid(self):
        return (self.birth_year is not None and
                1920 <= int(self.birth_year) <= 2002)

    def is_issue_year_valid(self):
        return (self.issue_year is not None and
                2010 <= int(self.issue_year) <= 2020)

    def is_expiration_year_valid(self):
        return (self.expiration_year is not None and
                2020 <= int(self.expiration_year) <= 2030)

    def is_height_valid(self):
        if self.height is None:
            return False
        if self.height.endswith("cm"):
            return 150 <= int(self.height[:-2]) <= 193
        if self.height.endswith("in"):
            return 59 <= int(self.height[:-2]) <= 76
        return False

    def is_hair_color_valid(self):
        return (self.hair_color is not None and
                re.fullmatch(r'#[0-9a-f]{6}', self.hair_color) is not None)

    def is_eye_color_valid(self):
        return (self.eye_color is not None and
                self.eye_color in ('amb', 'blu', 'brn', 'gry', 'grn',
                                   'hzl', 'oth'))

    def is_passport_id_valid(self):
        return (self.passport_id is not None and
                re.fullmatch(r'[0-9]{9}', self.passport_id) is not None)

    def is_data_valid(self):
        return (self.is_birth_year_valid() and self.is_issue_year_valid() and
                self.is_expiration_year_valid() and self.is_height_valid() and
                self.is_hair_color_valid() and self.is_eye_color_valid() and
                self.is_passport_id_valid())


def to_passports(raw_passport_data: list[str]) -> list[Passport]:
    grouped_data = itertools.groupby(raw_passport_data, lambda s: s != '')
    return [to_passport(p) for has_data, p in grouped_data if has_data]

def to_passport(passport: Iterable[str]) -> Passport:
    data_lookup: dict[str, Optional[str]] = defaultdict(lambda: None)
    for line in passport:
        for field in line.split(" "):
            name, value = field.split(":")
            data_lookup[name] = value
    return Passport(data_lookup["byr"],
                    data_lookup["iyr"],
                    data_lookup["eyr"],
                    data_lookup["hgt"],
                    data_lookup["hcl"],
                    data_lookup["ecl"],
                    data_lookup["pid"],
                    data_lookup["cid"])

def get_number_of_valid_passports(raw_passport_data: list[str]) -> int:
    passports = to_passports(raw_passport_data)
    return len([p for p in passports if p.is_valid()])

def get_number_of_valid_data_passports(raw_passport_data: list[str]) -> int:
    passports = to_passports(raw_passport_data)
    return len([p for p in passports if p.is_data_valid()])

PASSPORTS: list[str] = input_data.read("input/input4.txt")

if __name__ == "__main__":
    print(f"Number of valid passports: "
          f"{get_number_of_valid_passports(PASSPORTS)}")
    print(f"Number of data-valid passports: "
          f"{get_number_of_valid_data_passports(PASSPORTS)}")
