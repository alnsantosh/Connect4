import numpy as np
import random
from Player import Player
import math
from strategy import strategy

class strategyPlayer(Player):

    def __init__(self,myId,name="minMax Player"):
        self.name=name
        self.myId = myId


    def playMove(self,flattened_state,possible):

        for i in range(len(flattened_state)):
            if flattened_state[i] == 0:
                flattened_state[i] = -1
            elif flattened_state[i] == 1:
                flattened_state[i] = 2
            elif flattened_state[i] == 2:
                flattened_state[i] = 1

        s = np.reshape(flattened_state, (6,-1))
        state = s.tolist()   
        obj = strategy(state)
        if self.myId==1:
            best_move = obj.smartTurn1()
        else:
            best_move = obj.smartTurn0()
        return best_move