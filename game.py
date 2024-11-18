import numpy as np
import pickle
import random

#board is an array n x n where True values are not crossed balls and False values are crossed balls
#move is an array n x n where True values are not touched balls and False values are balls to be crossed

def createboard(n):
    return np.ones((n, n), dtype = bool)

def makeMove(move,board):
        return np.logical_and(board, move)

def spider(board):
    #returns all possible moves (not boards!)
    
    #vertical
    listofallmoves = []
    for n in range (len(board)):
        for m in range (len(board)):
            if board[n,m] == True:
                for k in range (len(board)):
                    if (m < (len(board)-k)):
                        if board[n,(len(board)-k-1)] == True:
                            boardx = np.ones((len(board), len(board)), dtype = bool)
                            boardx[n,m:(len(board)-k)] = False
                            listofallmoves.append(boardx)
    
    #horizontal
    for n in range (len(board)):
        for m in range (len(board)):
            if board[m,n] == True:
                for k in range (len(board)):
                    if (m < (len(board)-k-1)): #-1 due to repeate ones
                        if board[(len(board)-k-1),n] == True:
                            boardx = np.ones((len(board), len(board)), dtype = bool)
                            boardx[m:len(board)-k,n] = False
                            listofallmoves.append(boardx)
    #diagonal backward 
    for n in range (len(board)-1):
        for m in range (len(board)-1):
            if board[n,m] == True:
                #boardx = np.ones((len(board), len(board)), dtype = bool)
                for k in range (1,len(board)):
                    #boardx = np.ones((len(board), len(board)), dtype = bool)
                    if (n < (len(board)-k)) & (m < (len(board)-k)) :
                            if board[n+k,m+k] == True: # move?
                                    boardx = np.ones((len(board), len(board)), dtype = bool)
                                    for x in range(k+1):
                                    #boardx = np.ones((len(board), len(board)), dtype = bool)
                                            boardx[n+x,m+x] = False
                                    listofallmoves.append(boardx)

    #diagonal forward 
    for n in range (len(board)-1,0,-1):
        for m in range (len(board)-1):
            if board[n,m] == True:
                #boardx = np.ones((len(board), len(board)), dtype = bool)
                for k in range (1,len(board)):
                    #boardx = np.ones((len(board), len(board)), dtype = bool)
                    if (n-k >= 0) & (m < (len(board)-k)) :
                            if board[n-k,m+k] == True:
                                    boardx = np.ones((len(board), len(board)), dtype = bool)
                                    for x in range(k+1):
                                    #boardx = np.ones((len(board), len(board)), dtype = bool)
                                            boardx[n-x,m+x] = False
                                    listofallmoves.append(boardx) 

    return listofallmoves
def drawBoard(board):
    n = len(board)
    for x in range (n):
        for y in range (n):
            if board[x,y]: print('O',end=' ')
            else: print('X',end=' ')
        print('')
   
def boardnum(board):
    k = len(board)
    num = 0
    i=1
                               
    for n in range (k):
        for m in range (k):
            if board[n,m] == False:
                num = num+i
            i=i*2
    return num
def rotation2(b1):
        listofrots = []
        listofrots.append(boardnum(np.rot90(b1,1)))
        listofrots.append(boardnum(np.rot90(b1,2)))
        listofrots.append(boardnum(np.rot90(b1,3)))
        listofrots.append(boardnum(np.rot90(b1,4)))
        
        listofrots.append(boardnum(np.rot90(np.fliplr(b1),1)))
        listofrots.append(boardnum(np.rot90(np.fliplr(b1),2)))
        listofrots.append(boardnum(np.rot90(np.fliplr(b1),3)))
        listofrots.append(boardnum(np.rot90(np.fliplr(b1),4)))
        
        listofrots.append(boardnum(np.rot90(np.flipud(b1),1)))
        listofrots.append(boardnum(np.rot90(np.flipud(b1),2)))
        listofrots.append(boardnum(np.rot90(np.flipud(b1),3)))
        listofrots.append(boardnum(np.rot90(np.flipud(b1),4)))
        
        return max(listofrots) 
def loadSet3():
    with open('dict_w3x.bin','rb') as input:
        savedset = pickle.load(input)
    return savedset
def loadSet4():
    with open('dict_w4x.bin','rb') as input:
        savedset = pickle.load(input)
    return savedset
def loadSet5():
    with open('dict_w5x.bin','rb') as input:
        savedset = pickle.load(input)
    return savedset

def game(n1,p):
    n = n1
    i_curPlayer = p
    b1 = createboard(n)
    if n == 5: dictw = loadSet5()
    elif n == 4: dictw = loadSet4()
    elif n == 3: dictw = loadSet3()
    
    while np.sum(b1) > 1:
        if i_curPlayer < 0:
            print("Comp-1 is thinking...")
            lose = False
            rng = random.SystemRandom()
            bestChoice = makeMove(b1,rng.choice(spider(b1)))
            for move in spider(b1):
                if rotation2(makeMove(move,b1)) in dictw:
                    bestChoice = makeMove(move,b1)
                    lose = True
            if lose: print('-100')
            else: print('100')
            print("Comp -1 plays: ")
            drawBoard(bestChoice)
            b1 = bestChoice
            i_curPlayer *= -1

        if i_curPlayer > 0:
            print("board:")
            drawBoard(b1)
            print("your turn:")
            i_choice = getMove(n,b1)
            b1 = np.logical_xor(np.logical_and(i_choice, b1), b1)
            print("You play:")
            drawBoard(b1)
            i_curPlayer *= -1

        winCheck(b1, -i_curPlayer)
def getMove(n,b1):    
    Move = np.zeros((n, n), dtype = bool)
    
    print('pattern:')
    if n == 5:
        print(' 0  1  2  3  4')
        print(' 5  6  7  8  9')
        print('10 11 12 13 14')
        print('15 16 17 18 19')
        print('20 21 22 23 24')
    if n == 4:
        print(' 0  1  2  3')
        print(' 4  5  6  7')
        print(' 8  9 10 11')
        print('12 13 14 15')
    elif n == 3:
        print('0 1 2')
        print('3 4 5 ')
        print('6 7 8')
    elif n == 2:
        print('0 1')
        print('2 3')
    print('choose balls to cross out(including middles OXO + "0 1 2" -> XXX) when finish type x or enter')
    
    while 1:
        choice = input()
        if choice == 'x' or choice == '': break
        i = 0
        for x in range (n):
            for y in range (n):
                if i == int(choice):
                    Move[x,y] = True
                i = i + 1
    for legalMove in spider(b1):
        #if arrays are equal
        if not(np.logical_xor(legalMove, ~Move).any()):
            return Move

    print ('illegal move')
    return getMove(n,b1)
def winCheck(board, i_playerNum):
    i_sum = np.sum(board)
    if i_sum <= 1:
        if i_playerNum > 0:
            if i_sum == 0:
                print("\t You lose you crossed out last ball")
                print("COMP WINS!!!")
                None
            else:
                #print("\t You win comp  must cross out last ball")
                print("YOU WIN!!!")
        else:
            if i_sum == 0:
                #print("\t You win.. there are no balls left.")
                print("YOU WIN!!!")
            else:
                #print("\t You loose you must cross out last ball!")
                print("COMP WINS!!!")
        print("*" * 30)
    
        return 0
    return 1

if __name__ == '__main__':
    print("INSTRUCTIONS : game(n,p) n - size of the baord (2,3,4,5) {p = -1 -> comp statrs p= 1-> human starts}.")
