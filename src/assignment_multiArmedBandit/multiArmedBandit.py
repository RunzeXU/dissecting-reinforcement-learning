
# coding: utf-8

# In[25]:


import numpy as np


# In[18]:


class MultiArmedBandit:
    def __init__(self):
        """
        In this case, when you initialize this MultiArmedBandit instance, we assume it is a fixed two-armed bandit
        The winning probabilities [0.6, 0.8] will be assigned to these two arms randomly
        The reward rate will be 200%, eg. if you put 1 coin, play arm 0 and you win, you will get 2 coins
        """
        self.total_arms = 2
        self.reward_probability_distribution = np.random.choice([0.6, 0.8], 2, replace=False, p=[0.5,0.5])
        self.reward_rate = 2

    def play(self, armNo, inputCoin):
        """
        @param: armNo: arm number you pull, in this case, should be 0 / 1
                inputCoin: coins you put for this round of play
        @return: reward coins count if you win, otherwise return 0
        """
        if armNo >= self.total_arms:
            raise Exception("MULTI ARMED BANDIT][ERROR] the arm NO. " + str(armNo) + " is out of range, total arms: " +str(self.total_arms)+" please set 0/1 as argument")
        win_probability = self.reward_probability_distribution[armNo]
        lose_robability = 1.0-win_probability
        return self.reward_rate*inputCoin*np.random.choice(2, p=[lose_robability, win_probability])


