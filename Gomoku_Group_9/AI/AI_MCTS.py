import numpy as np
import copy
import random
from Game.Board import Board
from AI.MonteCarloTreeNode import TreeNode

import time


class AI_MCTS():

    def __init__(self, name="AI_MCTS", search_times=10000, greedy_value=5.0, is_output_running=True):
        self.root = None
        self.name = name
        self.search_times = search_times  
        self.greedy_value = greedy_value  
        self.is_output_running = is_output_running  

    def reset(self):
        self.root = TreeNode(prior_prob=1.0)

    def take_action(self, board: Board, is_output_action=True):
        if is_output_action:
            print("...Thinking...")

        self.reset()
        self.run(board, self.search_times)
        action, _ = self.root.choose_best_child(0)
        board.step(action)
        
        if is_output_action:
            print("AI player {0} moves ({1}, {2})".format(self.name, action[0], action[1]))

        return action

    def run(self, start_board: Board, times):
        for i in range(times):
            board = copy.deepcopy(start_board)
            print("\rrunning: {} / {}".format(i, times), end="")

            node = self.traverse(self.root, board)
            node_player = board.current_player

            winner = self.rollout(board)

            value = 0
            if winner == node_player:
                value = 1
            elif winner == -node_player:
                value = -1

            node.backpropagate(-value)

    def traverse(self, node: TreeNode, board: Board):
        """
        Expand node
        """
        while True:
            if len(node.children) == 0:
                break
            action, node = node.choose_best_child(c=self.greedy_value)
            board.step(action)

        is_over, _ = board.result()
        if is_over:
            return node

        actions = board.available_actions
        probs = np.ones(len(actions)) / len(actions)

        for action, prob in zip(actions, probs):
            _ = node.expand(action, prob)

        return node

    def rollout(self, board: Board):
        """
        :return: winner<int>
        """
        while True:
            is_over, winner = board.result()
            if is_over:
                break
            self.rollout_policy(board)
        return winner

    def rollout_policy(self, board: Board):
        """
        Decision function, random decision here.
        """

        action = random.choice(list(board.available_actions))

        board.step(action)
