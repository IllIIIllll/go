# © 2020 지성. all rights reserved.
# <llllllllll@kakao.com>
# MIT License

class Agent:
    def __init__(self):
        pass

    def select_move(self, game_state):
        raise NotImplementedError()

    def diagnostics(self):
        return {}