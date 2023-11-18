import gym
from gym import spaces
import numpy as np
import pandas as pd

class WeatherGenerationEnv(gym.Env):
    def __init__(self):
        super(WeatherGenerationEnv, self).__init__()

        self.action_space = spaces.Discrete(3)  
        self.observation_space = spaces.Box(low=0, high=100, shape=(5,), dtype=np.float32)


        self.weather_conditions = np.array([25.0, 50.0, 10.0, 1015.0, 10.0])  # initial temp, humidity, wind_speed, pressure, visibility


        self.data = pd.DataFrame(columns=['Temperature', 'Humidity', 'WindSpeed', 'Pressure', 'Visibility', 'Weather'])

    def step(self, action):
        if action == 0:
            self.weather_conditions += np.array([2.0, -5.0, 2.0, 0.0, 5.0])
            weather_type = 'Clear'
        elif action == 1:
            self.weather_conditions += np.array([-1.0, 2.0, -1.0, -2.0, -3.0])
            weather_type = 'Cloudy'
        elif action == 2:
            self.weather_conditions += np.array([-3.0, 5.0, -3.0, -5.0, -8.0])
            weather_type = 'Rainy'

        self.weather_conditions = np.clip(self.weather_conditions, 0, 100)

        new_row = pd.DataFrame({
            'Temperature': [self.weather_conditions[0]],
            'Humidity': [self.weather_conditions[1]],
            'WindSpeed': [self.weather_conditions[2]],
            'Pressure': [self.weather_conditions[3]],
            'Visibility': [self.weather_conditions[4]],
            'Weather': [weather_type]
            })

        self.data = pd.concat([self.data, new_row], ignore_index=True)

        reward = -np.sum(np.abs(self.weather_conditions - np.array([25.0, 50.0, 10.0, 1015.0, 10.0])))

        done = False

        info = {}

        return self.weather_conditions, reward, done, info

    def reset(self):
        self.weather_conditions = np.array([25.0, 50.0, 10.0, 1015.0, 10.0])
        return self.weather_conditions

    def render(self):
        print(f"Weather conditions: {self.weather_conditions}")

    def save_to_csv(self, filename='weather_data.csv'):
        self.data.to_csv(filename, index=False)

env = WeatherGenerationEnv()

state = env.reset()
print(f"Initial state: {state}")

for _ in range(100):  
    action = env.action_space.sample()
    state, reward, done, _ = env.step(action)
    print(f"Action: {action}, New state: {state}, Reward: {reward}")


env.save_to_csv('generated_weather_data.csv')


env.close()