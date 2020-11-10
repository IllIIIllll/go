# © 2020 지성. all rights reserved.
# <llllllllll@kakao.com>
# MIT License

import numpy as np

from dlgo.agent.base import Agent
from dlgo import goboard
from dlgo.agent.helpers import is_point_an_eye
from dlgo import kerasutil

class ACAgent(Agent):
    def __init__(self, model, encoder):
        self.model = model
        self.encoder = encoder
        self.collector = None
        self.last_state_value = 0

    def set_collector(self, collector):
        self.collector = collector

    def select_move(self, game_state):
        num_moves = self.encoder.board_width * self.encoder.board_height

        board_tensor = self.encoder.encode(game_state)
        X = np.array([board_tensor])

        actions, values = self.model.predict(X)
        move_probs = actions[0]
        estimated_value = values[0][0]

        eps = 1e-6
        move_probs = np.clip(move_probs, eps, 1 - eps)
        move_probs = move_probs / np.sum(move_probs)

        candidates = np.arange(num_moves)
        ranked_moves = np.random.choice(
            candidates, num_moves, replace=False, p=move_probs)
        for point_idx in ranked_moves:
            point = self.encoder.decode_point_index(point_idx)
            move = goboard.Move.play(point)
            move_is_valid = game_state.is_valid_move(move)
            fills_own_eye = is_point_an_eye(
                game_state.board, point,
                game_state.next_player
            )
            if move_is_valid and (not fills_own_eye):
                if self.collector is not None:
                    self.collector.record_decision(
                        state=board_tensor,
                        action=point_idx,
                        estimated_value=estimated_value
                    )
                return goboard.Move.play(point)
        return goboard.Move.pass_turn()

    def serialize(self, h5file):
        h5file.create_group('encoder')
        h5file['encoder'].attrs['name'] = self.encoder.name()
        h5file['encoder'].attrs['board_width'] = self.encoder.board_width
        h5file['encoder'].attrs['board_height'] = self.encoder.board_height
        h5file.create_group('model')
        kerasutil.save_model_to_hdf5_group(self.model, h5file['model'])