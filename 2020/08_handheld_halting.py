from typing import List


def main():
    parser = Parser("08.in")
    commands = parser.parse()
    executor = Executor(commands)

    # Part 1
    executor.run_until_loop_or_end()
    print(f"Part 1, accumulator: {executor.accumulator}")

    # Part 2 - fix the loop
    while True:
        # Undo until the previous nop/jmp and change it
        while True:
            executor.undo_step()

            if executor.next_command.function == "jmp":
                executor.next_command.function = "nop"
                break
            elif executor.next_command.function == "nop":
                executor.next_command.function = "jmp"
                break

        # Save executor state
        executor.save()

        # Try running again
        ran_to_the_end = executor.run_until_loop_or_end()
        if ran_to_the_end:
            break

        # Didn't reach the end, load the saved state
        executor.load()

        # Change back the function to the original
        if executor.next_command.function == "jmp":
            executor.next_command.function = "nop"
        elif executor.next_command.function == "nop":
            executor.next_command.function = "jmp"

    print(f"Part 2, accumulator: {executor.accumulator}")


class Command:
    def __init__(self, function: str, value: int) -> None:
        self.function = function
        self.value = value
        self.ran = False


class Parser:
    def __init__(self, filename: str) -> None:
        self.filename = filename

    def parse(self) -> List[Command]:
        commands: List[Command] = []

        with open(self.filename, "r") as file:
            for line in file.readlines():
                line = line.replace("\n", "")
                command = Parser._parse_line(line)
                commands.append(command)

        return commands

    @staticmethod
    def _parse_line(line: str) -> Command:
        function, value = line.split(" ")
        return Command(function, int(value))


class Executor:
    def __init__(self, commands: List[Command]) -> None:
        self.commands = commands
        self._states: List[ExecutorState] = []
        self.reset()

    def reset(self):
        self._save_position = 0
        self._states.append(ExecutorState(0, 0))
        for command in self.commands:
            command.ran = False

    def run_until_loop_or_end(self) -> bool:
        """Run the progarm until the end or it loops

        Returns:
            bool: True if the program ran to the end, false if it ran into a loop
        """
        while True:
            if len(self.commands) <= self.next:
                return True
            if self.commands[self.next].ran:
                return False

            self._step()

    def _step(self) -> None:
        """Execute the next command"""
        next_command = self.next_command

        if next_command.function == "acc":
            state = ExecutorState(self.next + 1, self.accumulator + next_command.value)
        elif next_command.function == "jmp":
            state = ExecutorState(self.next + next_command.value, self.accumulator)
        else:
            state = ExecutorState(self.next + 1, self.accumulator)

        self._states.append(state)
        next_command.ran = True

    def undo_step(self) -> None:
        self._states.pop()
        self.next_command.ran = False

    def save(self) -> None:
        """Save the current state"""
        self._save_position = len(self._states)

    def load(self) -> None:
        """Load the previous saved state"""
        # Undo until we are at the saved state
        while len(self._states) > self._save_position:
            self.undo_step()

        # Execute until we arrive at the saved state
        while len(self._states) < self._save_position:
            self._step()

    @property
    def accumulator(self) -> int:
        return self._states[-1].accumulator

    @property
    def next(self) -> int:
        return self._states[-1].next

    @property
    def next_command(self) -> Command:
        return self.commands[self.next]


class ExecutorState:
    def __init__(self, next: int, accumulator: int) -> None:
        self.next = next
        self.accumulator = accumulator


# Run program
main()
