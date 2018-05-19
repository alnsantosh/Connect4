from keras import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
import numpy as np
import random
from Player import Player
import math
import time

class RLPlayer(Player):
    

    # For self play we have to pass model
    def __init__(self, state_size, action_size, model,name="RL Player"):  
        #super(Player,self).__init__(name)
        self.move=1
        self.name=name
        self.model=model
        # will be 42
        self.memory = []
        # discount rate
        # Change epsilon size (experimental)
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.999


    def remember(self, state, action):
        self.memory.append((state, action))
    def playMove(self, state,possibleMoves):
        if self.move==1:
            if np.random.rand() <= self.epsilon:
                    return possibleMoves[random.randint(0,len(possibleMoves)-1)]
            act_values=[]
            for i in possibleMoves:
                act_values.append((i,self.model.predict(self.formatBoard(state,i))[0][0]))
            
            act_values.sort(key=lambda x:x[1])
            all_max=[]
            for i in act_values:
                if i[1]==act_values[0][1]:
                    all_max.append(i)
                else:
                    break
            if len(all_max)==1:
                return all_max[0][0]
            else:
                try:
                    x=all_max[random.randint(0,len(all_max)-1)][0]
                except Exception:
                    print(act_values)
                    print(all_max)
                    print(state)
                    print(possibleMoves)
                    return 0
                return x 
            #(math.floor(np.argmax(act_values[0])/7),np.argmax(act_values[0])%7)  # returns action

    def formatBoard(self,board,action):
        board[board==2]=-1
        a=np.zeros(7)
        a[action]=1
        iboard=np.asarray(board)
        inputboard=np.append(iboard,a)
        inputboard=np.reshape(inputboard, (1,42+7))
        return inputboard


    def replay(self,win):
        prevreward=win
        gamma=0.9
        for i in range(len(self.memory)-1,-1,-1):
            state, action=self.memory[i]
            currreward=prevreward
            if(i!=len(self.memory)-1):
                currreward= prevreward* gamma
            self.model.fit(self.formatBoard(state,action), [currreward], epochs=1, verbose=0)
            prevreward=currreward
        self.memory=[]
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

