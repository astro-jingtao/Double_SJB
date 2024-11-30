from player import Naive_DCJB_Player, Random_DCJB_Player


class Game:

    def __init__(self, game, player1, player2) -> None:
        self.game = game
        self.player1 = player1
        self.player2 = player2

    def play_step(self, auto_restart=True):
        if self.game.stage > self.game.FINAL_STAGE:
            if auto_restart:
                self.game.reset()
            else:
                raise ValueError("Game is over")

        observation = self.game.observe()

        a_action = self.player1.act(observation)
        b_action = self.player2.act(observation)

        reward_a, reward_b = self.game.step(a_action, b_action)

        return observation, a_action, b_action, reward_a, reward_b


class Double_CJB:
    '''
    1, 2, 3: chui, jian, bao
    0, 1: 
    -1, 0, 1:
    '''
    FINAL_STAGE = 2

    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self.a_state = [-1, -1, -1]
        self.b_state = [-1, -1, -1]
        self.stage = 0

    def check_action(self, a_action: int, b_action: int):
        # sourcery skip: swap-nested-ifs
        if self.stage < 2:
            if a_action not in [1, 2, 3] or b_action not in [1, 2, 3]:
                raise ValueError("In first two stages, Action must be 1, 2, 3")
        if self.stage == 2:
            if a_action not in [0, 1] or b_action not in [0, 1]:
                raise ValueError("In last stage, action must be 0, 1")

    def step(self, a_action: int, b_action: int):
        if self.stage > 2:
            raise ValueError("Game is over")
        self.check_action(a_action, b_action)
        self.a_state[self.stage] = a_action
        self.b_state[self.stage] = b_action
        self.stage += 1
        return self.get_reward()

    def observe(self):
        return self.a_state, self.b_state, self.stage

    def get_reward(self):
        if self.stage != 3:
            return 0, 0
        a_final = self.a_state[self.a_state[-1]]
        b_final = self.b_state[self.b_state[-1]]
        if a_final == b_final:
            return 0, 0
        elif (a_final == 1 and b_final == 2 or a_final == 2 and b_final == 3
              or a_final == 3 and b_final == 1):
            return 1, -1
        else:
            return -1, 1


if __name__ == '__main__':
    DCJB = Double_CJB()
    game = Game(DCJB, Random_DCJB_Player("A", 0), Naive_DCJB_Player("B", 1))

    r1_sum = 0
    r2_sum = 0

    for _ in range(3 * 10000):
        _, _, _, r1, r2 = game.play_step()
        r1_sum += r1
        r2_sum += r2

    print(r1_sum, r2_sum)
