# © 2020 지성. all rights reserved.
# <llllllllll@kakao.com>
# MIT License

from dlgo.goboard import Move
from dlgo.gotypes import Point

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