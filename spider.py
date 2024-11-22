import numpy as np

def spider(board):
    #vertical
    listofallmoves = []
    for n in range (len(board)):
        for m in range (len(board)):
            if board[n,m] == True:
                for k in range (len(board)):
                    if (m < (len(board)-k)):
                        if board[n,(len(board)-k-1)] == True:
                            boardx = np.ones((len(board), len(board)), dtype=bool)
                            boardx[n,m:(len(board)-k)] = False
                            listofallmoves.append(boardx)
    
    #horizontal
    for n in range (len(board)):
        for m in range (len(board)):
            if board[m,n] == True:
                for k in range (len(board)):
                    if (m < (len(board)-k-1)):
                        if board[(len(board)-k-1),n] == True:
                            boardx = np.ones((len(board), len(board)), dtype=bool)
                            boardx[m:len(board)-k,n] = False
                            listofallmoves.append(boardx)
    #diagonal backward 
    for n in range (len(board)-1):
        for m in range (len(board)-1):
            if board[n,m] == True:
                for k in range (1,len(board)):
                    if (n < (len(board)-k)) & (m < (len(board)-k)) :
                            if board[n+k,m+k] == True:
                                    boardx = np.ones((len(board), len(board)), dtype=bool)
                                    for x in range(k+1):
                                            boardx[n+x,m+x] = False
                                    listofallmoves.append(boardx)

    #diagonal forward 
    for n in range (len(board)-1,0,-1):
        for m in range (len(board)-1):
            if board[n,m] == True:
                for k in range (1,len(board)):
                    if (n-k >= 0) & (m < (len(board)-k)) :
                            if board[n-k,m+k] == True:
                                    boardx = np.ones((len(board), len(board)), dtype=bool)
                                    for x in range(k+1):
                                            boardx[n-x,m+x] = False
                                    listofallmoves.append(boardx) 
    return listofallmoves
