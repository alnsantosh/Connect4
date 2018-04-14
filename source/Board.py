
# coding: utf-8

# In[2]:


import numpy as np
import random


# In[7]:


class Board():
    def __init__(self):
        self.board=np.zeros((6,7))
        for i in range(7):
            self.board[5][i]=3
    
    def nextPossibleMove(self):
        a,b=np.where(self.board==3)
        return list(zip(a,b))
    
    def checkValidMove(self,r,c):
        return self.board[r][c]==3
    
    def makeMove(self,r,c,player):
        if self.checkValidMove(r,c):
            self.board[r][c]=player
            if r>0:
                self.board[r-1][c]=3
        return
    
    def checkFilled(self):
        flag=len(list(zip(np.where(self.board==0))))==0
        return flag
    
    

