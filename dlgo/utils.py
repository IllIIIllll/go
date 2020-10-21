# © 2020 지성. all rights reserved.
# <llllllllll@kakao.com>
# MIT License

from dlgo import gotypes

COLS = 'ABCDEFGHJKLMNOPQRST'
STONE_TO_CHAR = {
    None: ' . ',
    gotypes.Player.black: ' X ',
    gotypes.Player.white: ' O ',
}

# 다음 수 출력
def print_move(player, move):
    if move.is_pass:
        move_str = 'passes'
    elif move.is_resign:
        move_str = 'resigns'
    else:
        move_str = f'{COLS[move.point.col - 1]}{move.point.row}'
    print(f'{str(player)} {move_str}')

# 현재 바둑판 현황 출력
def print_board(board):
    for row in range(board.num_rows, 0, -1):
        bump = ' ' if row <= 9 else ''
        line = []
        for col in range(1, board.num_cols + 1):
            stone = board.get(gotypes.Point(row=row, col=col))
            line.append(STONE_TO_CHAR[stone])
        print(f'{bump}{row} {"".join(line)}')
    print(f'{"    "}{"  ".join(COLS[:board.num_cols])}')