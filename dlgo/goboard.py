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