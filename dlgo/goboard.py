# © 2020 지성. all rights reserved.
# <llllllllll@kakao.com>
# MIT License

# 자기 차례에 할 수 있는 행동 정의
class Move():
    def __init__(self, point=None, is_pass=False, is_resign=False):
        assert (point is not None) ^ is_pass ^ is_resign
        self.point = point
        self.is_play = self.point is not None
        self.is_pass = is_pass
        self.is_resign = is_resign

    # 바둑판에 돌을 놓는 행위
    @classmethod
    def play(cls, point):
        return Move(point=point)

    # 현재 차례를 넘기는 행위
    @classmethod
    def pass_turn(cls):
        return Move(is_pass=True)

    # 기권하는 행위
    @classmethod
    def resign(cls):
        return Move(is_resign=True)

# 이음 정의
class GoString():
    def __init__(self, color, stones, liberties):
        self.color = color
        self.stones = set(stones)
        self.liberties = set(liberties)

    def remove_liberty(self, point):
        self.liberties.remove(point)

    def add_liberty(self, point):
        self.liberties.add(point)

    # 두 선수의 이음의 모든 돌을 저장한 새 이음 반환
    def merged_with(self, go_string):
        assert go_string.color == self.color
        combined_stones = self.stones | go_string.stones
        return GoString(
            self.color,
            combined_stones,
            (self.liberties | go_string.liberties) - combined_stones
        )

    @property
    def num_liberties(self):
        return len(self.liberties)

    def __eq__(self, other):
        return isinstance(other, GoString) and \
            self.color == other.color and \
            self.stones == other.stones and \
            self.liberties == other.liberties