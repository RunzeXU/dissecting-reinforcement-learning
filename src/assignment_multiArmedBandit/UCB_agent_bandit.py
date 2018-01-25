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

#Average cumulated reward: 791.21
#Std Cumulated Reward: 13.2125281457
#Average utility distribution: [ 0.39188487  0.50654831  0.80154085]
#Average utility RMSE: 0.0531917417346

from multi_armed_bandit import MultiArmedBandit
import numpy as np
import math
def return_rmse(predictions, targets):
    """Return the Root Mean Square error between two arrays
    @param predictions an array of prediction values
    @param targets an array of target values
    @return the RMSE
    """
    return np.sqrt(((predictions - targets)**2).mean())

def return_ucb_action(arms_counter_array, arms_values_array):
    """Return an action using Thompson sampling
    @param success_counter_array (alpha) success rate for each action
    @param failure_counter_array (beta) failure rate for each action
    @return the action selected
    """
    ubc_values = arms_values_array + np.sqrt(np.true_divide(2*math.log(sum(arms_counter_array)), arms_counter_array))
    #beta_sampling_array = np.random.beta(success_counter_array, failure_counter_array)
    return np.argmax(ubc_values)

def main():
    reward_distribution = [0.3, 0.5, 0.8]
    my_bandit = MultiArmedBandit(reward_probability_list=reward_distribution)
    tot_arms = 3
    tot_episodes = 2000
    tot_steps = 1000
    print_every_episodes = 100
    cumulated_reward_list = list()
    average_utility_array = np.zeros(tot_arms)
    print("Starting Thompson agent...")
    for episode in range(tot_episodes):
        cumulated_reward = 0
        arms_counter_array = np.ones(tot_arms)
        arms_values_array = np.zeros(tot_arms)
        success_counter_array = np.ones(tot_arms)
        failure_counter_array = np.ones(tot_arms)
        #success_counter_array = [10, 10, 10]
        #failure_counter_array = [10, 10, 10]
        action_counter_array = np.full(tot_arms, 1.0e-5)
        for step in range(tot_steps):
            action = return_ucb_action(arms_counter_array, arms_values_array)
            reward = my_bandit.step(action)
            arms_counter_array[action] += 1
            arms_values_array = np.multiply(np.true_divide((arms_counter_array - 1), arms_counter_array), arms_values_array) + 1/np.ones(tot_arms)*reward
            if reward == 1:
                success_counter_array[action] += 1
            elif reward == 0:
                failure_counter_array[action] += 1
            else:
                raise Exception("Wrong value returned as Reward...")
            action_counter_array[action] += 1
            cumulated_reward += reward
        # Append the cumulated reward for this episode in a list
        cumulated_reward_list.append(cumulated_reward)
        utility_array = np.true_divide(np.add(success_counter_array,[-1,-1,-1]), action_counter_array)
        average_utility_array += utility_array
        if episode % print_every_episodes == 0:
            print("Episode: " + str(episode))
            print("Cumulated Reward: " + str(cumulated_reward))
            print("Success counter: " + str(np.add(success_counter_array,[-1,-1,-1])))
            print("Failure counter: " + str(np.add(failure_counter_array, [-1,-1,-1])))
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

"string"
