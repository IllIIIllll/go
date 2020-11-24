# © 2020 지성. all rights reserved.
# <llllllllll@kakao.com>
# MIT License

import numpy as np

from dlgo.agent.base import Agent

class AlphaGoNode:
    def __init__(self, parent=None, probability=1.0):
        self.parent = parent
        self.children = {}

        self.visit_count = 0
        self.q_value = 0
        self.prior_value = probability
        self.u_value = probability

    def select_child(self):
        return max(self.children.items(),
                   key=lambda child: child[1].q_value + child[1].u_value)

    def expand_children(self, moves, probabilities):
        for move, prob in zip(moves, probabilities):
            if move not in self.children:
                self.children[move] = AlphaGoNode(probability=prob)

    def update_values(self, leaf_value):
        if self.parent is not None:
            self.parent.update_values(leaf_value)

        self.visit_count += 1

        self.q_value += leaf_value / self.visit_count

        if self.parent is not None:
            c_u = 5
            self.u_value = c_u * np.sqrt(self.parent.visit_count) \
                * self.prior_value / (1 + self.visit_count)

class AlphaGoMCTS(Agent):
    def __init__(self, policy_agent, fast_policy_agent, value_agent,
                 lambda_value=0.5, num_simulations=1000,
                 depth=50, rollout_limit=100):
        self.policy = policy_agent
        self.rollout_policy = fast_policy_agent
        self.value = value_agent

        self.lambda_value = lambda_value
        self.num_simulations = num_simulations
        self.depth = depth
        self.rollout_limit = rollout_limit
        self.root = AlphaGoNode()

    def select_move(self, game_state):
        for simulation in range(self.num_simulations):
            current_state = game_state
            node = self.root
            for depth in range(self.depth):
                if not node.children:
                    if current_state.is_over():
                        break
                    moves, probabilities = self.policy_probabilities(current_state)
                    node.expand_children(moves, probabilities)

                move, node = node.select_child()
                current_state = current_state.apply_move(move)

            value = self.value.predict(current_state)
            rollout = self.policy_rollout(current_state)

            weighted_value = (1 - self.lambda_value) * value + \
                self.lambda_value * rollout

            node.update_values(weighted_value)