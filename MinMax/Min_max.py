import numpy as np
import matplotlib.pyplot as plt
import time

board = [' ', 'o', 'o', ' ', 'x', ' ', 'x', ' ', ' ']

def printBoard(board):
    print(board[0] + "|" + board[1] + "|" + board[2])
    print(board[3] + "|" + board[4] + "|" + board[5])
    print(board[6] + "|" + board[7] + "|" + board[8])
    print("\n")

def CheckDraw(board):
    for el in board:
        if el == ' ':
            return False
    
    return True

def CheckWin(board, mark):
    if (board[0] == board[1] and board[0] == board[2] and board[0] == mark):
        return True
    elif (board[3] == board[4] and board[3] == board[5] and board[3] == mark):
        return True
    elif (board[6] == board[7] and board[6] == board[8] and board[6] == mark):
        return True
    elif (board[0] == board[3] and board[0] == board[6] and board[0] == mark):
        return True
    elif (board[1] == board[4] and board[1] == board[7] and board[1] == mark):
        return True
    elif (board[2] == board[5] and board[2] == board[8] and board[2] == mark):
        return True
    elif (board[0] == board[4] and board[0] == board[8] and board[0] == mark):
        return True
    elif (board[6] == board[4] and board[6] == board[2] and board[6] == mark):
        return True
    else:
        return False

def max_value(board, alfa , beta):
    #Return score
    if CheckWin(board, 'o') == True: 
        return -1
    elif CheckDraw(board) == True:
        return 0
    ##############

    v = float('-inf')

    #Children creation#
    t = []
    b_temp = board.copy()
    for idx in range(len(b_temp)):
        if b_temp[idx] == ' ':
            b_temp[idx] = 'x'
            t.append(b_temp.copy())
            b_temp[idx] = ' '
        else:
            continue
    ################

    for el in t:
        v = max(v, min_value(el, alfa, beta))
        alfa = max(alfa, v)
        if alfa >= beta:
            return v
    return v


def min_value(board, alfa, beta):
    #Return score
    if CheckWin(board,'x') == True:
        return 1
    elif CheckDraw(board) == True:
        return 0
    #############

    v = float('inf')
   
    #Children creation
    t = []
    b_temp = board.copy()
    for idx in range(len(b_temp)):
        if b_temp[idx] == ' ':
            b_temp[idx] = 'o'
            t.append(b_temp.copy())
            b_temp[idx] = ' '
        else:
            continue
    ################

    for el in t:
        v = min(v, max_value(el, alfa, beta))
        beta = min(beta, v)
        if alfa >= beta:
            return v
    return v

# print("Jeżeli jest ruch O to: ")
# if min_value(board) == -1:
#     print("O wygrywa!")
# elif min_value(board) == 1:
#     print("X wygrywa!")
# else:
#     print("Remis!")

# print("Jeżeli jest ruch X to: ")
# if max_value(board) == 1:
#     print("O wygrywa!")
# elif max_value(board) == -1:
#     print("X wygrywa!")
# else:
#     print("Remis!")

print(min_value(board, -1, 1))