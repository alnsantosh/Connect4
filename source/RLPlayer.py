import numpy
import random
import import_ipynb
from Player import Player


class RLPlayer(Player):
    

    # For self play we have to pass model
    def __init__(self, state_size, action_size,name="RL Player"):  
        super(RandomPlayer,self).__init__(name)
        self.state_size = state_size
        self.action_size = action_size

        #Change memory size (experimental) 
        self.memory = deque(maxlen=2000)

        #Change gamma size (experimental)
        self.gamma = 0.95    # discount rate

        #Change epsilon size (experimental)
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.model = self._build_model()
    def _build_model(self):
        # Neural Net for Deep-Q learning Model

        ## Develop based on structure
        model = Sequential()
        model.add(Dense(24, input_dim=self.state_size, activation='relu'))
        model.add(Dense(24, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse',
                      optimizer=Adam(lr=self.learning_rate))
        return model
    def remember(self, state, action, reward, next_state, done):
        #Maybe optimize
        self.memory.append((state, action, reward, next_state, done))
    def playmove(self, state,):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])  # returns action
    def replay(self, batch_size):
        #Not major changes
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
              target = reward + self.gamma * np.amax(self.model.predict(next_state)[0])
            target_f = self.model.predict(state)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay