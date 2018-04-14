
# coding: utf-8

# In[1]:


import numpy as np
import random
import import_ipynb
from Board import Board
from RandomPlayer import RandomPlayer


# In[12]:


class Game():
    def __init__(self, player1, player2):
        self.winner=None
        self.completed=False
        self.win_direction=None
        self.win_point=None
        self.p=[None,None]
        self.board=Board()
        if random.random()>0.5:
            self.p[0]=player1
            self.p[0].move=1
            self.p[1]=player2
            self.p[1].move=2
        else:
            self.p[0]=player2
            self.p[0].move=1
            self.p[1]=player1
            self.p[1].move=2
        print("Welcome to Connect4")
        print("Player 1 (X) is " + self.p[0].name)
        print("Player 2 (O) is " + self.p[1].name)
        
    
    def verticalCheck(self,r,c):
        win=False
        if 6-r>=4:
            win=True
            for i in range(4):
                if self.board.board[r][c]!=self.board.board[r+i][c]:
                    win=False
                    break
        if win:
            self.win_direction='vertical'
        return win
    
    def horizontalCheck(self,r,c):
        win=False
        if 7-c>=4:
            win=True
            for i in range(4):
                if self.board.board[r][c]!=self.board.board[r][c+i]:
                    win=False
                    break
        if win:
            self.win_direction='horizontal'
        return win
    
    def positiveDiagonalCheck(self,r,c):
        win=False
        if 6-r>=4 and 7-c>=4:
            win=True
            for i in range(4):
                if self.board.board[r][c]!=self.board.board[r+i][c+i]:
                    win=False
                    break
        if win:
            self.win_direction='positiveDiagonal'
        return win
    
    def negativeDiagonalCheck(self,r,c):
        win=False
        if 6-r>=4 and 7-c<=4:
            win=True
            for i in range(4):
                if self.board.board[r][c]!=self.board.board[r+i][c-i]:
                    win=False
                    break
        if win:
            self.win_direction='negativeDiagonal'
        return win
    
    def findWinner(self):
        for r in range(6):
            for c in range(7):
                if self.board.board[r][c]!=3 and self.board.board[r][c]!=0:
                    win= self.verticalCheck(r,c) or self.horizontalCheck(r,c) or self.positiveDiagonalCheck(r,c) or self.negativeDiagonalCheck(r,c)
                    if win:
                        self.winner=self.board.board[r][c]
                        self.completed=True
                        self.win_point=(r,c)
                        return
    
    def run(self):
        move=0
        while not self.completed and not self.board.checkFilled():
            flatten_board=self.board.board.flatten()
            possible=self.board.nextPossibleMove()
            p=self.p[move].playMove(flatten_board,possible)
            r=p[0]
            c=p[1]
            if not self.board.checkValidMove(r,c):
                print("Invalid Move")
                print("Game ends")
                return
            self.board.makeMove(r,c,move+1)
            self.findWinner()
            if move:
                move=0
            else:
                move=1
        print(self.winner)
        print(self.board.board)
        print(self.win_direction)
        print(self.win_point)
    


# In[14]:


a=Game(RandomPlayer(),RandomPlayer())
a.run()
