import random


class Player:

    def __init__(self, name, side) -> None:
        self.name = name
        self.side = side

    def act(self, observation):
        raise NotImplementedError


class Random_DCJB_Player(Player):
    # random strategy

    def act(self, observation):
        return random.randint(1, 3) if observation[2] < 2 else random.randint(
            0, 1)


class Naive_DCJB_Player(Player):
    '''
    naive strategy: 
    - random in the first round
    - avoid repeat in the second round
    - select the best action assume the opponent is playing randomly in the last round
    '''

    def act(self,
            observation):  # sourcery skip: assign-if-exp, reintroduce-else
        a_state, b_state, stage = observation
        my_state = a_state if self.side == 0 else b_state
        you_state = b_state if self.side == 0 else a_state
        if stage == 0:
            return random.randint(1, 3)
        if stage == 1:
            if my_state[0] == 1:
                return random.choice([2, 3])
            if my_state[0] == 2:
                return random.choice([1, 3])
            if my_state[0] == 3:
                return random.choice([1, 2])
        if stage == 2:
            select0 = sum([
                check_win(my_state[0], you_state[0]),
                check_win(my_state[0], you_state[1])
            ])
            select1 = sum([
                check_win(my_state[1], you_state[0]),
                check_win(my_state[1], you_state[1])
            ])
            if select0 > select1:
                return 0
            if select0 < select1:
                return 1
            return random.randint(0, 1)


class Clever_DCJB_Player(Player):
    ...


class Equilibrium_DCJB_Player(Player):
    ...


def check_win(state_a, state_b):
    diff = state_a - state_b
    if diff == 0:
        return 0
    if diff in [1, -2]:
        return -1
    if diff in [-1, 2]:
        return 1
