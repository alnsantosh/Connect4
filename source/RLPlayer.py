from collections import deque
from keras import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
import numpy as np
import random
import import_ipynb
from Player import Player
import math

class RLPlayer(Player):
    

    # For self play we have to pass model
    def __init__(self, state_size, action_size, model,name="RL Player"):  
        #super(Player,self).__init__(name)
        self.name=name
        self.state_size = state_size
        self.model=model
        # will be 42
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        # discount rate
        self.gamma = 0.95
        # Change epsilon size (experimental)
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001


    def remember(self, state, action, reward, next_state, done):
        #Maybe optimize
        self.memory.append((state, action, reward, next_state, done))
    def playMove(self, state,possibleMoves):

        if np.random.rand() <= self.epsilon:
            return possibleMoves[random.randint(0,len(possibleMoves)-1)]
        act_values = self.model.predict(self.formatBoard(state))
        #print(act_values)
        return possibleMoves[random.randint(0,len(possibleMoves)-1)]
        #(math.floor(np.argmax(act_values[0])/7),np.argmax(act_values[0])%7)  # returns action

    def formatBoard(self,board):
        iboard=self.encoded(self.rearrange_player(board))
        iboard=np.asarray(iboard)
        iboard=np.reshape(iboard, (1,168))
        return iboard

    def rearrange_player(self,board):
        if self.move != 1:
            board[board == 1] = -1
            board[board == 2] = 1
            board[board == -1] = 2
        return board

    def encoded(self,board):
        e_board=[]
        for i in board:
            if i==0:
                e_board.extend([1,0,0,0])
            elif i==1:
                e_board.extend([0,1,0,0])
            elif i==2:
                e_board.extend([0,0,1,0])
            else:
                e_board.extend([0,0,0,1])
        return e_board


    def replay(self, batch_size):
        if batch_size>len(self.memory):
            mini_batch = random.sample(self.memory, len(self.memory))
        else:
            mini_batch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in mini_batch:
            target = reward
            train=self.formatBoard(next_state)
            act_values=self.model.predict(train)
            if not done:
                target = reward + self.gamma * np.amax(self.model.predict(train))
            if target!=0 and np.argmax(act_values[0])!="nan":
                #print(state,np.argmax(act_values[0]),target,next_state,done)
                print(act_values)
                self.remember(state,np.argmax(act_values[0]),target,next_state,done)
            currstate=self.formatBoard(state)
            target_f = self.model.predict(currstate)
            target_f[0][action] = target
            self.model.fit(currstate, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

