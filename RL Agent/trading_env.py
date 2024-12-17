import gymnasium
from gymnasium import spaces
import numpy as np
import pandas as pd

class TradingEnv(gym.Env):
    """
    Custom OpenAI Gym environment for stock/crypto trading.
    """
    metadata = {'render.modes': ['human']}

    def __init__(self, data, initial_balance=10000):
        super(TradingEnv, self).__init__()

        # Environment parameters
        self.data = data.reset_index(drop=True)
        self.initial_balance = initial_balance

        # Define action and observation space
        self.action_space = spaces.Discrete(3)  # Actions: 0=Hold, 1=Buy, 2=Sell
        self.observation_space = spaces.Box(
            low=-np.inf, high=np.inf, shape=(len(self.data.columns) + 2,), dtype=np.float32
        )

        # Internal state
        self.current_step = 0
        self.balance = self.initial_balance
        self.shares_held = 0
        self.total_profit = 0

    def reset(self):
        """
        Reset the environment to the initial state.
        """
        self.current_step = 0
        self.balance = self.initial_balance
        self.shares_held = 0
        self.total_profit = 0
        return self._next_observation()

    def _next_observation(self):
        """
        Return the current state space (features for the agent).
        """
        obs = np.array(self.data.iloc[self.current_step].values.tolist() +
                       [self.balance, self.shares_held])
        return obs

    def step(self, action):
        """
        Execute one step in the environment.
        :param action: The action to take.
        """
        # Get the current price
        current_price = self.data.iloc[self.current_step]['close']

        # Perform action
        if action == 1:  # Buy
            shares_to_buy = self.balance // current_price
            self.balance -= shares_to_buy * current_price
            self.shares_held += shares_to_buy

        elif action == 2:  # Sell
            self.balance += self.shares_held * current_price
            self.shares_held = 0

        # Move to the next step
        self.current_step += 1
        done = self.current_step >= len(self.data) - 1

        # Calculate reward
        total_asset_value = self.balance + self.shares_held * current_price
        reward = total_asset_value - self.initial_balance
        self.total_profit = total_asset_value - self.initial_balance

        return self._next_observation(), reward, done, {}

    def render(self, mode='human'):
        """
        Render the environment (print details).
        """
        current_price = self.data.iloc[self.current_step]['close']
        print(f"Step: {self.current_step}")
        print(f"Balance: {self.balance}")
        print(f"Shares Held: {self.shares_held}")
        print(f"Current Price: {current_price}")
        print(f"Total Profit: {self.total_profit}")
