from __future__ import annotations
from typing import Iterable, Sequence


class Sudoku:
    """A mutable sudoku puzzle."""

    def __init__(self, puzzle: Iterable[Iterable]):
        self._grid: list = []
        self._grid_column: list = []
        self._grid_block: list = []

        # Filling the grid with values in puzzle
        for puzzle_row in puzzle:
            row = []

            for element in puzzle_row:
                row.append(int(element))

            self._grid.append(row)

        # Filling the columns grid by using values in grid and reversing them
        for i in range(9):
            column = []
            for j in range(9):
                column.append(self._grid[j][i])

            self._grid_column.append(column)

        # Filling block grid using the grid
        for i in range(9):
            block = []
            x_start = (i % 3) * 3
            y_start = (i // 3) * 3
            for x in range(x_start, x_start + 3):
                for y in range(y_start, y_start + 3):
                    block.append(self._grid[y][x])
            self._grid_block.append(block)

    def place(self, value: int, x: int, y: int) -> None:
        """Place value at x,y."""
        self._grid[y][x] = int(value)

        # Changing value at column grid
        self._grid_column[x][y] = int(value)

        # Changing value in block grid
        block_index = (y // 3) * 3 + x // 3
        block_list_index = (x % 3) * 3 + y % 3
        self._grid_block[block_index][block_list_index] = int(value)

    def unplace(self, x: int, y: int) -> None:
        """Remove (unplace) a number at x,y."""
        self._grid[y][x] = 0

        # Changing value at column grid to 0
        self._grid_column[x][y] = 0

        # Changing value at block grid to 0
        block_index = (y // 3) * 3 + x // 3
        block_list_index = (x % 3) * 3 + y % 3
        self._grid_block[block_index][block_list_index] = 0

    def value_at(self, x: int, y: int) -> int:
        """Returns the value at x,y."""
        value = self._grid[y][x]

        return value

    def options_at(self, x: int, y: int) -> Iterable[int]:
        """Returns all possible values (options) at x,y."""
        options = {1, 2, 3, 4, 5, 6, 7, 8, 9}

        # Get the index of the block based from x,y
        block_index = (y // 3) * 3 + x // 3

        # Remove all values from row, column and block from options
        options = options - set(self.row_values(y)) - set(self.column_values(x)) - set(self.block_values(block_index))

        return options

    def next_empty_index(self) -> tuple[int, int]:
        """
        Returns the next index (x,y) that is empty (value 0).
        If there is no empty spot, returns (-1,-1)
        """
        next_x, next_y = -1, -1

        for y in range(9):
            if 0 in self._grid[y]:
                for x in range(9):
                    if self._grid[y][x] == 0:
                        return x, y

        return next_x, next_y

    def row_values(self, i: int) -> Iterable[int]:
        """Returns all values at i-th row."""
        return self._grid[i]

    def column_values(self, i: int) -> Iterable[int]:
        """Returns all values at i-th column."""
        return self._grid_column[i]

    def block_values(self, i: int) -> Iterable[int]:
        """
        Returns all values at i-th block.
        The blocks are arranged as follows:
        0 1 2
        3 4 5
        6 7 8
        """
        return self._grid_block[i]

    def is_solved(self) -> bool:
        """
        Returns True if and only if all rows, columns and blocks contain
        only the numbers 1 through 9. False otherwise.
        """
        values = {1, 2, 3, 4, 5, 6, 7, 8, 9}

        result = True

        for i in range(9):
            if values != set(self.column_values(i)):
                return False

            if values != set(self.row_values(i)):
                return False

            if values != set(self.block_values(i)):
                return False

        return result

    def __str__(self) -> str:
        representation = ""

        for row in self._grid:
            representation += ''.join(str(i) for i in row) + "\n"

        return representation.strip()


def load_from_file(filename: str) -> Sudoku:
    """Load a Sudoku from filename."""
    puzzle: list[str] = []

    with open(filename) as f:
        for line in f:

            # strip newline and remove all commas
            line = line.strip().replace(",", "")

            puzzle.append(line)

    return Sudoku(puzzle)
