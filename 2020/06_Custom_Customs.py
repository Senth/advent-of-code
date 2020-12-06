from typing import Dict


count = 0

# Part 1
with open("06.in", "r") as file:
    group_unique = set()
    for line in file.readlines():
        line = line.replace("\n", "")
        # New group
        if line == "":
            count += len(group_unique)
            group_unique = set()

        # Read unique answered yes questions
        else:
            for char in line:
                group_unique.add(char)
count += len(group_unique)

print(f"Part 1, count: {count}")


# Part 2
def count_yes(group_answers: Dict[str, int], person_count: int) -> int:
    yes = 0
    for count in group_answers.values():
        if count == person_count:
            yes += 1
    return yes


count = 0
person_count = 0
with open("06.in", "r") as file:
    group_answers = {}
    for line in file.readlines():
        line = line.replace("\n", "")

        # New group
        if line == "":
            count += count_yes(group_answers, person_count)
            group_answers = {}
            person_count = 0

        # Read answers
        else:
            person_count += 1
            for char in line:
                # Increase question yes count
                if char in group_answers:
                    group_answers[char] += 1
                else:
                    group_answers[char] = 1

count += count_yes(group_answers, person_count)
print(f"Part 2, count: {count}")