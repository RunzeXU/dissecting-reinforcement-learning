import numpy as np
from multiArmedBandit import MultiArmedBandit

def main():
    """
    in this assignment, you should complete a simulator to play a two-armed bandit, by designing a strategy to earn more reward
    the conditions are:
        you have 100 coins in each episode
        you are able to play maximum 30 rounds in each episode
        you are able to simulate 100 episodes then calculate the average reward

    :return: please print you final average reward coins after the simulation to verify how good your strategy is
    """
    total_episodes = 100
    total_coins = 100
    total_rounds = 30

    # the module 'MultiArmedBandit' has been imported, when you initial a MultiArmedBandit instance, a two-armed bandit has been created with the winning probability[60%, 80%]
    # however you do not know which arm has the higher. you are able to call 'play' function to simulate inputing coins and pulling one of these arms
    # eg. my_bandit.play(0,1) means pulling the first arm with 1 coin, if you win, 2 will be returned, representing you are reward double coins; otherwise it will return 0 if you lose.
    my_bandit = MultiArmedBandit()
    """
    #a basic strategy is provided here:
            
        implementation example: 
            1. play arm 1 at first 10 rounds and calculate total award
            2. play arm 2 at second 10 rounds and calculate total award
            3. choose the better award arm, then put all left coins in last 10 rounds
    """
    total_award_list = list()
    for episode in range(total_episodes):
        total_coins = 100
        arm1_test_reward = 0
        arm2_test_reward = 0
        input_coins_per_round = 1
        for playInArm1 in range(10):
            reward = my_bandit.play(0, input_coins_per_round)
            arm1_test_reward += (reward - input_coins_per_round)
            total_coins = total_coins + reward - input_coins_per_round
        for playInArm2 in range(10):
            reward= my_bandit.play(1, input_coins_per_round)
            arm2_test_reward += (reward - input_coins_per_round)
            total_coins = total_coins + reward - input_coins_per_round

        for leftRound in range(10):
            if(arm1_test_reward >= arm2_test_reward):
                total_coins = total_coins - np.floor(total_coins/10) + my_bandit.play(0, np.floor(total_coins/10))
            else:
                total_coins = total_coins - np.floor(total_coins/10) + my_bandit.play(1, np.floor(total_coins/10))
        print('in episode ' + str(episode+1)+' the final coins after 30 rounds are '+ str(total_coins))
        total_award_list.append(total_coins)
    # Print the average cumulated reward for all the episodes
    print("Average cumulated reward: " + str(np.mean(total_award_list)))




if __name__ == "__main__":
    main()
