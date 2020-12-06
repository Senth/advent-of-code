import re

regex = r"(\d+)-(\d+) ([a-z]): ([a-z]+)"

# Part 1
def is_valid_password_part1(line: str) -> bool:
    match = re.match(regex, line)
    if match:
        min, max, char, password = match.groups()
        min = int(min)
        max = int(max)
        char_count = password.count(char)
        return min <= char_count and char_count <= max
    return False


def is_valid_password_part2(line: str) -> bool:
    match = re.match(regex, line)
    if match:
        min, max, char, password = match.groups()
        min = int(min) - 1
        max = int(max) - 1
        found_count = 0

        if password[min] == char:
            found_count += 1
        if password[max] == char:
            found_count += 1

        return found_count == 1
    return False


valid_passwords_part1 = 0
valid_passwords_part2 = 0

with open("02.in", "r") as file:
    for line in file.readlines():
        if is_valid_password_part1(line):
            valid_passwords_part1 += 1
        if is_valid_password_part2(line):
            valid_passwords_part2 += 1

print(f"Part 1, valid passwords: {valid_passwords_part1}")
print(f"Part 2, valid passwords: {valid_passwords_part2}")