# © 2020 지성. all rights reserved.
# <llllllllll@kakao.com>
# MIT License

class Encoder:
    # 변환기 이름 로깅
    def name(self):
        raise NotImplementedError()

    # 바둑판을 숫자 데이터로 변환
    def encode(self, game_satate):
        raise NotImplementedError()

    # 바둑판의 점을 정수형 인덱스로 변환
    def encode_point(self, point):
        raise NotImplementedError

    # 정수형 인덱스를 바둑판의 점으로 변환
    def decode_point(self, index):
        raise NotImplementedError

    # 점의 갯수
    def num_points(self):
        raise NotImplementedError

    # 변환된 바둑판의 모양
    def shape(self):
        raise NotImplementedError