#!/usr/bin/env python

# MIT License
# Copyright (c) 2017 Massimiliano Patacchiola
# https://mpatacchiola.github.io/blog/
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

#Average cumulated reward: 648.0975
#Std Cumulated Reward: 16.1566083616
#Average utility distribution: [ 0.29889418  0.49732589  0.79993241]
#Average utility RMSE: 0.0016711564118

from multi_armed_bandit import MultiArmedBandit
import numpy as np

def return_rmse(predictions, targets):
    """Return the Root Mean Square error between two arrays

    @param predictions an array of prediction values
    @param targets an array of target values
    @return the RMSE
    """
    return np.sqrt(((predictions - targets)**2).mean())

def boltzmann(x, temperature):
    """Compute boltzmann distribution of array x.

    @param x the input array
    @param temperature
    @return the boltzmann array
    """
    exponent = np.true_divide(x - np.max(x), temperature)
    return np.exp(exponent) / np.sum(np.exp(exponent))
    
def return_boltzmann_action(temperature, reward_counter_array):
    """Return an action using an epsilon greedy strategy

    @return the action selected
    """
    tot_arms = reward_counter_array.shape[0]
    boltzmann_distribution = boltzmann(reward_counter_array, temperature)
    return np.random.choice(tot_arms, p=boltzmann_distribution)

def main():
    reward_distribution = [0.3, 0.5, 0.8]
    my_bandit = MultiArmedBandit(reward_probability_list=reward_distribution)
    temperature_start = 0.1
    temperature_stop = 0.0001
    epsilon = 0.1
    tot_arms = 3
    tot_episodes = 2000
    tot_steps = 1000
    print_every_episodes = 100
    cumulated_reward_list = list()
    average_utility_array = np.zeros(tot_arms)
    temperature_array = np.linspace(temperature_start, temperature_stop, num=tot_steps)
    print("Starting Boltzmann agent...")
    for episode in range(tot_episodes):
        cumulated_reward = 0
        reward_counter_array = np.zeros(tot_arms)
        action_counter_array = np.full(tot_arms, 1.0e-5)
        for step in range(tot_steps):
            temperature = temperature_array[step]
            action = return_boltzmann_action(temperature, np.true_divide(reward_counter_array, action_counter_array))
            reward = my_bandit.step(action)
            reward_counter_array[action] += reward 
            action_counter_array[action] += 1      
            cumulated_reward += reward
        # Append the cumulated reward for this episode in a list
        cumulated_reward_list.append(cumulated_reward)
        utility_array = np.true_divide(reward_counter_array, action_counter_array)
        average_utility_array += utility_array
        if episode % print_every_episodes == 0:
            print("Episode: " + str(episode))
            print("Cumulated Reward: " + str(cumulated_reward))
            print("Reward counter: " + str(reward_counter_array))
            print("Utility distribution: " + str(utility_array))
            print("Utility RMSE: " + str(return_rmse(utility_array, reward_distribution)))
            print("")
    # Print the average cumulated reward for all the episodes
    print("Average cumulated reward: " + str(np.mean(cumulated_reward_list)))
    print("Std Cumulated Reward: " + str(np.std(cumulated_reward_list)))
    print("Average utility distribution: " + str(average_utility_array / tot_episodes))
    print("Average utility RMSE: " + str(return_rmse(average_utility_array/tot_episodes, reward_distribution)))

if __name__ == "__main__":
    main()
