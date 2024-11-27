from itertools import combinations
from spider import *

def createboard(n):
    return np.ones((n, n), dtype=np.bool_)

def number_to_array(number, n):
    return np.array([*str(bin(number))[2:].rjust(n*n, "0")]).astype(np.bool_)

def show_board(board, n):
    return(board.reshape(n,n).astype(np.uint8))

def possible_moves(board, kernels, n):
    moved_boards = set(np.sum(np.logical_and(kernels, board) * 2 ** np.arange(n**2-1, -1, -1), axis=1))
    moved_boards.discard(np.sum(board * 2 ** np.arange(n**2-1, -1, -1)))
    moved_boards.discard(0)
    return moved_boards