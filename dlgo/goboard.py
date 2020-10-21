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

# 바둑판 정의
class Board():
    def __init__(self, num_rows, num_cols):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self._grid = {}

    # 활로 파악용 이웃한 점 확인
    def place_stone(self, player, point):
        assert self.is_on_grid(point)
        assert self._grid.get(point) is None
        adjacent_same_color = []
        adjacent_opposite_color = []
        liberties = []
        for neighbor in point.neighbors():
            if not self.is_on_grid(neighbor):
                continue
            neighbor_string = self._grid.get(neighbor)
            if neighbor_string is None:
                liberties.append(neighbor)
            elif neighbor_string.color == player:
                if neighbor_string not in adjacent_same_color:
                    adjacent_same_color.append(neighbor_string)
            else:
                if neighbor_string not in adjacent_opposite_color:
                    adjacent_opposite_color.append(neighbor_string)
        new_string = GoString(player, [point], liberties)

        # 같은 색의 근접한 이음 병합
        for same_color_string in adjacent_same_color:
            new_string = new_string.merged_with(same_color_string)
        for new_string_point in new_string.stones:
            self._grid[new_string_point] = new_string
        # 다른 색의 근접한 이음의 활로 삭제
        for other_color_string in adjacent_opposite_color:
            other_color_string.remove_liberty(point)
        # 다른 색 이음의 활로가 0이면 돌 제거
        for other_color_string in adjacent_opposite_color:
            if not other_color_string.num_liberties:
                self._remove_string(other_color_string)

    def _remove_string(self, string):
        for point in string.stones:
            for neighbor in point.neighbors():
                neighbor_string = self._grid.get(neighbor)
                if neighbor_string is None:
                    continue
                if neighbor_string is not string:
                    neighbor_string.add_liberty(point)
            self._grid[point] = None

    def is_on_grid(self, point):
        return 1 <= point.row <= self.num_rows and \
            1 <= point.col <= self.num_cols

    # 해당 좌표에 돌이 있으면 색을 반환
    # 돌이 없으면 None을 반환
    def get(self, point):
        string = self._grid.get(point)
        if string is None:
            return None
        return string.color

    # 해당 좌표에 돌이 있으면 연결된 모든 이음 반환
    # 돌이 없으면 None을 반환
    def get_go_string(self, point):
        string = self._grid.get(point)
        if string is None:
            return None
        return string