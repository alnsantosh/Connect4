import numpy as np
import random


# In[7]:


class Board():
    def __init__(self):
        self.board=np.zeros((6,7))
    
    def nextPossibleMove(self):
        x=[]
        for i in range(len(self.board[0])):
            if self.board[0][i]==0:
                x.append(i)
        return x
    
    def checkValidMove(self,c):
        x=self.nextPossibleMove()
        if c in x:
            return True
        return False
    
    def makeMove(self,c,player):
        if self.checkValidMove(c):
            for i in range(0,7):
                if i==6:
                    self.board[5][c]=player
                    return
                if self.board[i][c]!=0:
                    self.board[i-1][c]=player
                    break
    
    def checkFilled(self):
        flag=len(list(zip(np.where(self.board==0))))==0
        return flag
    
    

