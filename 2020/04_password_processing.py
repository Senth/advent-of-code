from __future__ import annotations
import re
from types import FunctionType, LambdaType
from typing import Dict, List, Pattern


class Passport:
    _required_fields: Dict[str] = {
        "byr": lambda value: Passport._validate_number(value, 1920, 2002),
        "iyr": lambda value: Passport._validate_number(value, 2010, 2020),
        "eyr": lambda value: Passport._validate_number(value, 2020, 2030),
        "hgt": lambda value: Passport._validate_height(value),
        "hcl": lambda value: Passport._validate_color(value),
        "ecl": lambda value: Passport._validate_eye_color(value),
        "pid": lambda value: re.match(r"^\d{9}$", value) != None,
    }

    def __init__(self) -> None:
        self._fields: Dict[str] = {}

    def add_fields(self, line: str) -> None:
        fields = line.split(" ")

        for field in fields:
            name, value = field.split(":")
            self._fields[name] = value

    def has_all_required_fields(self) -> bool:
        for required_field in Passport._required_fields:
            if required_field not in self._fields:
                return False
        return True

    def is_valid_format(self) -> bool:
        for required_field, is_valid_function in Passport._required_fields.items():
            if required_field not in self._fields:
                return False

            value = self._fields[required_field]
            if not is_valid_function(value):
                return False

        return True

    @staticmethod
    def _validate_number(value_str: str, min: int, max: int) -> bool:
        try:
            value = int(value_str)
            return min <= value and value <= max
        except:
            return False

    @staticmethod
    def _validate_height(value: str) -> bool:
        match = re.match(r"^(\d+)(cm|in)$", value)
        if match:
            length = match.group(1)
            unit = match.group(2)

            if unit == "cm":
                return Passport._validate_number(length, 150, 193)
            elif unit == "in":
                return Passport._validate_number(length, 59, 76)

        return False

    @staticmethod
    def _validate_color(value: str) -> bool:
        return re.match(r"^#[a-f0-9]{6}$", value) != None

    @staticmethod
    def _validate_eye_color(value: str) -> bool:
        if value == "amb":
            return True
        if value == "blu":
            return True
        if value == "brn":
            return True
        if value == "gry":
            return True
        if value == "grn":
            return True
        if value == "hzl":
            return True
        if value == "oth":
            return True
        return False


# Parse passports
passports: List[Passport] = []
with open("04.in", "r") as file:
    passport = Passport()

    for line in file.readlines():
        line = line.replace("\n", "")

        # New passport
        if line == "":
            passports.append(passport)
            passport = Passport()

        # Add fields to passport
        else:
            passport.add_fields(line)

# Add last passport
passports.append(passport)

# Count valid passports
valid_passports = 0
for passport in passports:
    if passport.has_all_required_fields():
        valid_passports += 1

print(f"Part 1, valid passports: {valid_passports}")

# Full validation
valid_passports = 0
for passport in passports:
    if passport.is_valid_format():
        valid_passports += 1
print(f"Part 2, valid passports: {valid_passports}")
