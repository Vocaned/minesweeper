import random
import typing

class Cell:
    def __init__(self, value: int = 0, hidden: bool = True) -> None:
        """Creates a cell.

        @value: Cell's value. -1 = mine, 0-8
        @hidden: Whether the cell's value is currently hidden.
        @flag: Whether the cell has a flag on it.
        """
        self.value = value
        self.hidden = hidden
        self.flag = False

class Board:
    def __init__(self, width: int, height: int, mines: int) -> None:
        """Initializes a board with settings. Generates a board.

        @width: Board's width
        @height: Board's height
        @mines: Number of mines on the board."""
        if mines > width*height:
            # More mines than cells on the board
            raise ValueError(mines)

        self.width = width
        self.height = height
        self.mines = mines
        self.cells = []
        self.alive = False

        self.generate()

    def revealall(self) -> None:
        for row in range(self.height):
            for column in range(self.width):
                self.cells[row][column].hidden = False

    def reveal(self, x: int, y: int) -> None:
        """Reveals a cell on the board.
        If a bomb is revealed, Board.Alive is set to False.
        If a blank cell is revealed, all connected blank cells are also revealed.
        """
        cell = self.cells[y][x]

        if not cell.hidden:
            return # Cell has already been revealed

        if cell.flag:
            return # Cell has a flag on it

        cell.hidden = False

        if cell.value == -1:
            self.alive = False # Cell was a bomb, kill the board.

        if cell.value == 0:
            # Recursively reveal blank cells
            neighbours = self.checkneighbours(x, y, None)
            for x2, y2 in neighbours:
                self.reveal(x2, y2)

    def checkcell(self, x: int, y: int, value: int) -> bool:
        """Checks if cell in `(x,y)` matches `value`.

        If `value` is none, just checks if the cell is valid without checking the value."""
        if y < 0 or y >= self.height or \
           x < 0 or x >= self.width:
            return False

        if not value:
            return True

        return self.cells[y][x].value == value


    def checkneighbours(self, x: int, y: int, value: int) -> typing.List[typing.Tuple[int, int]]:
        """Checks all neighbouring cells of `(x, y)` and returns a list of cells that match `value`"""
        matches = []

        if self.checkcell(x-1, y-1, value):
            matches.append((x-1, y-1)) # top-left
        if self.checkcell(x, y-1, value):
            matches.append((x, y-1)) # top
        if self.checkcell(x+1, y-1, value):
            matches.append((x+1, y-1)) # top-right
        if self.checkcell(x-1, y, value):
            matches.append((x-1, y)) # left
        if self.checkcell(x+1, y, value):
            matches.append((x+1, y)) # right
        if self.checkcell(x-1, y+1, value):
            matches.append((x-1, y+1)) # bottom-left
        if self.checkcell(x, y+1, value):
            matches.append((x, y+1)) # bottom
        if self.checkcell(x+1, y+1, value):
            matches.append((x+1, y+1)) # bottom-right

        return matches

    def generate(self) -> None:
        """Generates a minesweeper board and stores it in Board.cells"""
        # Clear previous board
        self.cells = []
        tmpcells = []

        # Generate a blank board
        for _ in range(self.height * self.width):
            tmpcells.append(Cell())

        # Generates mines
        minepositions = random.sample(tmpcells, self.mines)
        for cell in minepositions:
            cell.value = -1

        # Turn cell list into a 2d array
        for row in range(self.height):
            cellrow = []
            for column in range(self.width):
                cellrow.append(tmpcells[row*self.width+column])
            self.cells.append(cellrow)

        # Calculate rest of the cells values
        for row in range(self.height):
            for column in range(self.width):
                if self.cells[row][column].value == -1:
                    continue # Don't calculate neighbours from bombs
                self.cells[row][column].value = len(self.checkneighbours(column, row, -1))

        self.alive = True
