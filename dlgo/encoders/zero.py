# © 2020 지성. all rights reserved.
# <llllllllll@kakao.com>
# MIT License

import numpy as np

from dlgo.goboard import Move
from dlgo.gotypes import Point, Player

# 1. 활로가 1개인 자신의 돌
# 2. 활로가 2개인 자신의 돌
# 3. 활로가 3개인 자신의 돌
# 4. 활로가 4개 이상인 자신의 돌
# 5. 활로가 1개인 상대의 돌
# 6. 활로가 2개인 상대의 돌
# 7. 활로가 3개인 상대의 돌
# 8. 활로가 4개 이상인 상대의 돌
# 9. 자신이 흰 돌일 경우 1로 채운 평면
# 10. 상대가 흰 돌일 경우 1로 채운 평면
# 11. 패가 되는 수
class ZeroEncoder:
    def __init__(self, board_size):
        self.board_size = board_size
        self.num_planes = 11

    def encode_move(self, move):
        if move.is_play:
            return (self.board_size * (move.point.row - 1) +
                (move.point.col - 1))
        elif move.is_pass:
            return self.board_size * self.board_size
        raise ValueError('Cannot encode resign move')

    def decode_move_index(self, index):
        if index == self.board_size * self.board_size:
            return Move.pass_turn()
        row = index // self.board_size
        col = index % self.board_size
        return Move.play(Point(row=row + 1, col=col + 1))

    def num_moves(self):
        return self.board_size * self.board_size + 1

    def encode(self, game_state):
        board_tensor = np.zeros(self.shape())
        next_player = game_state.next_player
        if game_state.next_player == Player.white:
            board_tensor[8] = 1
        else:
            board_tensor[9] = 1
        for r in range(self.board_size):
            for c in range(self.board_size):
                p = Point(row=r + 1, col=c + 1)
                go_string = game_state.board.get_go_string(p)

                if go_string is None:
                    if game_state.does_move_violate_ko(next_player,
                                                       Move.play(p)):
                        board_tensor[10][r][c] = 1
                else:
                    liberty_plane = min(4, go_string.num_liberties) - 1
                    if go_string.color != next_player:
                        liberty_plane += 4
                    board_tensor[liberty_plane][r][c] = 1

        return board_tensor

    def shape(self):
        return self.num_planes, self.board_size, self.board_size