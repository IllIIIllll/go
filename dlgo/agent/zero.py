# © 2020 지성. all rights reserved.
# <llllllllll@kakao.com>
# MIT License

class Branch:
    def __init__(self, prior):
        self.prior = prior
        self.visit_count = 0
        self.total_value = 0.0