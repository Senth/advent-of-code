from typing import Dict, List, Set, Tuple


class BoardingCard:
    def __init__(self, value: str) -> None:
        self._value = value
        self.row = BoardingCard._binary_to_int(value[:-3], "B")
        self.column = BoardingCard._binary_to_int(value[-3:], "R")

    @staticmethod
    def _binary_to_int(binary: str, on_char: str) -> int:
        converted_bin = ""
        for char in binary:
            if char == on_char:
                converted_bin += "1"
            else:
                converted_bin += "0"

        return int(converted_bin, base=2)

    @property
    def seat_id(self) -> int:
        return self.row * 8 + self.column


boarding_cards: List[BoardingCard] = []
occupied_spaces: Set[int] = set()
seat_id_max = 0

# Parse Boarding Passes
with open("05.in", "r") as file:
    for line in file.readlines():
        line = line.replace("\n", "")
        boarding_card = BoardingCard(line)
        seat_id = boarding_card.seat_id

        if seat_id_max < seat_id:
            seat_id_max = seat_id

        boarding_cards.append(boarding_card)
        occupied_spaces.add(seat_id)

print(f"Max seat id: {seat_id_max}")

missing_spaces: List[int] = []
for i in range(seat_id_max + 1):
    if i not in occupied_spaces:
        missing_spaces.append(i)

print(f"Missing spaces: {missing_spaces}")