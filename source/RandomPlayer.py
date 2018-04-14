
# coding: utf-8

# In[2]:


import numpy
import random
import import_ipynb
from Player import Player


# In[3]:


class RandomPlayer(Player):
    def __init__(self):
        super(RandomPlayer,self).__init__()
        self.name="Random Player"
    
    def playMove(self,board,possibleMoves):
        return possibleMoves[random.randint(0,len(possibleMoves)-1)]

