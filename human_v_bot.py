# © 2020 지성. all rights reserved.
# <llllllllll@kakao.com>
# MIT License

from dlgo import agent
from dlgo import goboard
from dlgo import gotypes
from dlgo.utils import print_board, print_move, point_from_coords

import time

def main():
    board_size = 9
    game = goboard.GameState.new_game(board_size)
    bot = agent.naive.RandomBot()

    while not game.is_over():
        try:
            print_board(game.board)
            if game.next_player == gotypes.Player.black:
                human_move = input('placement : ')
                point = point_from_coords(human_move.strip())
                move = goboard.Move.play(point)
            else:
                move = bot.select_move(game)

            print_move(game.next_player, move)
            game = game.apply_move(move)
        except ValueError:
            print('Please enter the correct point')
        except IndexError:
            print('Please enter the correct point')
        except AssertionError:
            print('It is a illegal point.')

if __name__ == '__main__':
    main()