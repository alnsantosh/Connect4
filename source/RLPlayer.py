from collections import deque
import random
from keras import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
import numpy as np


class RLPlayer:
    def __init__(self,state_size,action_size):
        self.name = "RL_player"
        # will be 168
        self.state_size = state_size
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
        self.model = self._build_model()

    def _build_model(self):
        model = Sequential()
        model.add(Dense(42, input_dim=self.state_size, activation='relu'))
        model.add(Dense(42, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse',
                      optimizer=Adam(lr=self.learning_rate))
        return model

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])  # returns action

    def rearrage_player(self,board,move):
        if move != 1:
            board[board == 1] = -1
            board[board == 2] = 1
            board[board == -1] = 2
        return board

    def remember(self,state,action,reward,next_state,completed):
        #needs to be optimized
        self.memory.append((state, action, reward, next_state, completed))

    def replay(self, batch_size):
        mini_batch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, completed in mini_batch:
            target = reward
            if not completed:
                target = reward + self.gamma * np.amax(self.model.predict(next_state)[0])
            target_f = self.model.predict(state)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

