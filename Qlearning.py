import numpy as np
from TaquinGame import State
from TaquinGame import Action
import random


class Qlearning:
    gamma = 0.95
    epsilon_range = (1, 0.1)
    max_iter = 50

    def __init__(self):
        self.world = State(30)
        self.q_matrix = {}

    def q_value(self, state, action):
        if state + (action.value,) in self.q_matrix:
            return self.q_matrix[state + (action.value,)]

        #random_q = random.uniform(0, 1)
        #self.q_matrix[state + (action.value,)] = random_q
        #return random_q
        return 0

    def max_q_value(self, state):
        max_q = -1
        best_action = None

        for action in self.world.actions():
            q = self.q_value(state, action)
            if q > max_q:
                max_q = q
                best_action = action

        return max_q, best_action

    def epsilon_policy(self, epsilon):
        # Best move
        if random.uniform(0, 1) >= epsilon:
            max_q, action = self.max_q_value(self.world.get_state())
            return action
        # Random
        else:
            return self.world.random_action()

    def episode(self, epsilon):
        self.world.initialize()
        iter = 0

        while not self.world.goal_achieved():
            action = self.epsilon_policy(epsilon)
            old_state = self.world.get_state()
            self.world.do_action(action)
            new_state = self.world.get_state()
            max_q, best_action = self.max_q_value(new_state)
            self.q_matrix[old_state + (action.value,)] = self.world.reward() + self.gamma * max_q

            if iter >= self.max_iter:
                self.world.initialize()
                iter = 0
            else:
                iter += 1

    def learn_q(self, episodes):
        epsilons = np.linspace(self.epsilon_range[0], self.epsilon_range[1], num=episodes)

        for i, epsilon in enumerate(epsilons):
            print("Episode ", i+1, "/", episodes)
            self.episode(epsilon)

        for i in range(20):
            print("Episode ", i + 1, "/", 20)
            self.episode(self.epsilon_range[1])
            print("Number iter :", self.evaluate())

    def evaluate(self):
        iter = 0
        self.world.initialize()
        while not self.world.goal_achieved():
            max_q, action = self.max_q_value(self.world.get_state())
            self.world.do_action(action)

            if iter >= 5000:
                break
            iter += 1

        return iter

    def run(self):
        self.world.initialize()
        print()
        print("Path :")
        self.world.show()

        while not self.world.goal_achieved():
            max_q, action = self.max_q_value(self.world.get_state())
            print("q value of best action:", max_q)
            self.world.do_action(action)
            self.world.show()
