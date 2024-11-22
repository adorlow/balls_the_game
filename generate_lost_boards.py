from itertools import combinations
from spider import *

def createboard(n):
    return np.ones((n, n), dtype=np.bool_)

def number_to_array(number, n):
    return np.array([*str(bin(number))[2:].rjust(n*n, "0")]).astype(np.bool_)

def k_balls_combinations(k, n):
    return set(np.sum(np.array(list(combinations(2**np.arange(n*n), k))), axis=1))

def iswin(board, lost_boards, n, kernels):
    board = number_to_array(board, n)
    # kernels application
    moved_boards = set(np.sum(np.logical_and(kernels, board) * 2 ** np.arange(0, n**2), axis=1))
    moved_boards.discard(np.sum(board * 2 ** np.arange(0, n**2)))
    
    for b in moved_boards:
        if b in lost_boards:
            return False
    return True

def genList(n):
    lost_boards = k_balls_combinations(1, n)
    board = createboard(n=n)
    kernels = np.bool_(spider_flat(board))
    
    for k in range(3, n**2+1):
        cmbs = k_balls_combinations(k, n)
        for num_board in cmbs:
            if iswin(num_board, lost_boards, n, kernels):
                lost_boards.add(num_board)
    return lost_boards

###################################################################################################################
###################################################################################################################
###################################################################################################################

from time import time

start_time = time()
genList(n=3)
print("--- %s seconds ---" % (time() - start_time))

start_time = time()
genList(n=4)
print("--- %s seconds ---" % (time() - start_time))

#lost_boards = genList(n=3)
#2**n**2 -1 - np.array(list(lost_boards))
