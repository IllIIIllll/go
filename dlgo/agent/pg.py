# © 2020 지성. all rights reserved.
# <llllllllll@kakao.com>
# MIT License

import numpy as np

from dlgo.agent.base import Agent
from dlgo import kerasutil
from dlgo import encoders
from dlgo.agent.helpers import is_point_an_eye
from dlgo import goboard

def clip_probs(original_probs):
    min_p = 1e-5
    max_p = 1 - min_p
    clipped_probs = np.clip(original_probs, min_p, max_p)
    clipped_probs = clipped_probs / np.sum(clipped_probs)
    return clipped_probs

class PolicyAgent(Agent):
    def __init__(self, model, encoder):
        self.model = model
        self.encoder = encoder

    def serialize(self, h5file):
        h5file.create_group('encoder')
        h5file['encoder'].attrs['name'] = self.encoder.name()
        h5file['encoder'].attrs['board_width'] = self.encoder.board_width
        h5file['encoder'].attrs['board_height'] = self.encoder.board_height
        h5file.create_group('model')
        kerasutil.save_model_to_hdf5_group(self.model, h5file['model'])

    def set_collector(self, collector):
        self.collector = collector

    def select_move(self, game_state):
        board_tensor = self.encoder.encode(game_state)
        X = np.array([board_tensor])
        move_probs = self.model.predict(X)[0]

        move_probs = clip_probs(move_probs)

        num_moves = self.encoder.board_width * self.encoder.board_height
        candidates = np.arange(num_moves)
        ranked_moves = np.random.choice(
            candidates,
            num_moves,
            replace=False,
            p=move_probs
        )
        for point_idx in ranked_moves:
            point = self.encoder.decode_point_index(point_idx)
            move = goboard.Move.play(point)
            is_valid = game_state.is_valid_move(move)
            is_an_eye = is_point_an_eye(
                game_state.board,
                point,
                game_state.next_player
            )
            if self.collector is not None:
                self.collector.record_decision(
                    state=board_tensor,
                    action=point_idx
                )
            return goboard.Move.play(point)
        return goboard.Move.pass_turn()

def load_policy_agent(h5file):
    model = kerasutil.load_model_from_hdf5_group(h5file['model'])
    encoder_name = h5file['encoder'].attrs['name']
    board_width = h5file['encoder'].attrs['board_width']
    board_height = h5file['encoder'].attrs['board_height']
    encoder = encoders.get_encoder_by_name(
        encoder_name,
        (board_width, board_height)
    )
    return PolicyAgent(model, encoder)