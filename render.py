import math
import tkinter
import utils
import typing

class TkinterBackend:
    CELLSIZE = 16
    def __init__(self, board: utils.Board) -> None:
        """Creates a Tkinter window for the minesweeper board.

        @board: The minesweeper board instance to render.
        """

        self.board = board

        self.top = tkinter.Tk()
        self.canvas = tkinter.Canvas(self.top, bg='black', height=self.board.width*self.CELLSIZE, width=self.board.height*self.CELLSIZE)

        self.canvas.bind("<Button-1>", self.leftbutton)
        self.canvas.bind("<Button-3>", self.rightbutton)
        self.canvas.pack()

        self.render()

        self.top.mainloop()

    def render(self):
        for row in range(self.board.height):
            for column in range(self.board.width):
                cell = self.board.cells[column][row]
                color = 'white'
                if cell.flag:
                    color = 'red'
                elif cell.hidden:
                    color = 'gray'
                else:
                    if cell.value == -1:
                        color = 'black'
                    elif cell.value == 0:
                        color = 'white'
                    elif cell.value == 1:
                        color = 'green'
                    elif cell.value == 2:
                        color = 'blue'
                    elif cell.value == 3:
                        color = 'green'
                    else:
                        color = 'magenta'

                self.canvas.create_rectangle(row*self.CELLSIZE, column*self.CELLSIZE, (row+1)*self.CELLSIZE, (column+1)*self.CELLSIZE, fill=color)

    def px2cellcoords(self, x: int, y: int) -> typing.Tuple[int, int]:
        """Turns mouse coordinates (pixels) to cell coordinates"""
        x = math.floor(x/self.CELLSIZE)
        y = math.floor(y/self.CELLSIZE)

        # Fix out of bounds clicking on far-right and far-bottom sides of the grid
        x = self.board.width if x > self.board.width else x
        y = self.board.height if y > self.board.height else y

        return (x, y)

    def leftbutton(self, event):
        x, y = self.px2cellcoords(event.x, event.y)
        self.board.reveal(x, y)

        if not self.board.alive:
            self.board.revealall()

        self.render()

    def rightbutton(self, event):
        x, y = self.px2cellcoords(event.x, event.y)
        cell = self.board.cells[y][x]
        cell.flag = not cell.flag # Toggle flag

        self.render()

class EmojiBackend:
    substitute = {
        -1: '\N{BOMB}',
        0: '\N{WHITE LARGE SQUARE}',
        1: '\U00000031\U000020E3',
        2: '\U00000032\U000020E3',
        3: '\U00000033\U000020E3',
        4: '\U00000034\U000020E3',
        5: '\U00000035\U000020E3',
        6: '\U00000036\U000020E3',
        7: '\U00000037\U000020E3',
        8: '\U00000038\U000020E3'
    }

    def __init__(self, board: utils.Board) -> None:
        for row in range(board.height):
            rowvalues = ''
            for column in range(board.width):
                rowvalues += str(self.substitute[board.cells[row][column].value])
            print(rowvalues)

class TextBackend:
    def __init__(self, board: utils.Board) -> None:
        for row in range(board.height):
            rowvalues = ''
            for column in range(board.width):
                val = str(board.cells[row][column].value)
                if val == '-1':
                    val = 'x'
                rowvalues += val
            print(rowvalues)
