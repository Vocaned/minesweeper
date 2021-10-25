import utils
import render

if __name__ == '__main__':
    board = utils.Board(9, 9, 10)
    render.TkinterBackend(board)
