
# coding: utf-8

# In[2]:


import numpy
import random
import import_ipynb
from Player import Player


# In[3]:


class RandomPlayer(Player):
    def __init__(self,move,name="Random Player"):
        super(RandomPlayer,self).__init__(name)
    
    def playMove(self,board,possibleMoves):
        return possibleMoves[random.randint(0,len(possibleMoves)-1)]

