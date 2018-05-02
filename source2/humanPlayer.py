import numpy as np
import random
from Player import Player
import math

class humanPlayer(Player):

    def __init__(self,myId,name="human Player"):
        self.name=name
        self.myId = myId


    def playMove(self,flattened_state,possible):
        s = np.reshape(flattened_state, (6,-1))
        self.displayBoard(s)
        print("Enter the column you would like to place your move: ")
        col = int(input())
        while col not in list(range(1,8)):
            print("You entered an invalid move. Please enter the column in the range 1 to 7: ")
            col = int(input())
        return col-1 

    
    def displayBoard(self,board):
        print("  | 1 | 2 | 3 | 4 | 5 | 6 | 7 |")
        for i in range(0,6):
            print("%d " % (i+1),end="", flush = True)
            for j in range(0,7):
                if j<6:
                    print("%s %s %s" % ('|', int(board[i][j]), ''), end="", flush = True)
                else:
                    print("%s %s %s" % ('|', int(board[i][j]), '|'), end="", flush = True)
            print(end="\n")
        print("\n")