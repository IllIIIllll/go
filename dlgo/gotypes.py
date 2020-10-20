# © 2020 지성. all rights reserved.
# <llllllllll@kakao.com>
# MIT License

import enum

class Player(enum.Enum):
    black = 1
    white = 2

    @property
    def other(self):
        return Player.black if self == Player.white else Player.white