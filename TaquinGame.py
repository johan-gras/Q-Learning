import numpy as np
from enum import Enum


class Action(Enum):
    haut = 0
    droite = 1
    bas = 2
    gauche = 3


class State:
    goal_reward = 200
    array = None
    final = None
    empty = None
    initial_actions = None

    def __init__(self, initial_actions = -1):
        self.initial_actions = initial_actions
        self.initialize()

        self.final = np.arange(9).reshape(3, 3)
        self.final = np.append(np.arange(1, 9), [0]).reshape(3, 3)

    def initialize(self):
        nb_actions = self.initial_actions
        if nb_actions == -1:
            self.array = np.array([1, 8, 2, 0, 4, 3, 7, 6, 5]).reshape(3, 3)
            self.empty = (0, 1)
        else:
            self.array = np.arange(9).reshape(3, 3)
            self.array = np.append(np.arange(1, 9), [0]).reshape(3, 3)
            self.empty = (2, 2)
            for i in range(nb_actions):
                action = self.random_action()
                self.do_action(action)


    def goal_achieved(self):
        return np.array_equal(self.array, self.final)

    def show(self):
        print(self.array)
        print()

    def isSame(self, state):
        return np.array_equal(self.array, state.array)

    def actions(self):
        actions = [Action.bas, Action.haut, Action.gauche, Action.droite]
        x, y = self.empty

        if x == 0:
            actions.remove(Action.gauche)
        elif x == 2:
            actions.remove(Action.droite)
        if y == 0:
            actions.remove(Action.haut)
        elif y == 2:
            actions.remove(Action.bas)

        return actions

    def random_action(self):
        actions = self.actions()
        index = np.random.randint(0, len(actions))
        return actions[index]

    def get_state(self):
        return tuple(map(tuple, self.array))

    def reward(self):
        if self.goal_achieved():
            return self.goal_reward
        return 0

    def shape_state(self):
        return self.array.shape

    def shape_action(self):
        return (4)

    def do_action(self, action):
        x, y = self.empty

        if action == Action.haut:
            self.array[y][x] = self.array[y - 1][x]
            self.array[y - 1][x] = 0
            self.empty = x, y-1

        elif action == Action.bas:
            self.array[y][x] = self.array[y + 1][x]
            self.array[y + 1][x] = 0
            self.empty = x, y+1

        elif action == Action.droite:
            self.array[y][x] = self.array[y][x + 1]
            self.array[y][x + 1] = 0
            self.empty = x+1, y

        elif action == Action.gauche:
            self.array[y][x] = self.array[y][x - 1]
            self.array[y][x - 1] = 0
            self.empty = x-1, y
