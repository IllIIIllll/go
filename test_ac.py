# © 2020 지성. all rights reserved.
# <llllllllll@kakao.com>
# MIT License

import argparse
import h5py

from tensorflow.keras.layers import Conv2D, Dense, Flatten, Input
from tensorflow.keras.models import Model

from dlgo import rl
from dlgo import encoders

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--board-size', type=int, default=19)
    parser.add_argument('output_file')
    args = parser.parse_args()

    encoder = encoders.get_encoder_by_name('simple', args.board_size)

    board_input = Input(shape=encoder.shape(), name='board_input')

    conv1 = Conv2D(
        64,
        (3, 3),
        padding='same',
        activation='relu'
    )(board_input)
    conv2 = Conv2D(
        64,
        (3, 3),
        padding='same',
        activation='relu'
    )(conv1)
    conv3 = Conv2D(
        64,
        (3, 3),
        padding='same',
        activation='relu'
    )(conv2)

    flat = Flatten()(conv3)
    processed_board = Dense(512)(flat)

    policy_hidden_layer = Dense(
        512,
        activation='relu'
    )(processed_board)
    policy_output = Dense(
        encoder.num_points(),
        activation='softmax'
    )(policy_hidden_layer)

    value_hidden_layer = Dense(
        512,
        activation='relu'
    )(processed_board)
    value_output = Dense(
        1,
        activation='tanh'
    )(value_hidden_layer)

    model = Model(
        inputs=board_input,
        outputs=[policy_output, value_output]
    )

    new_agent = rl.ACAgent(model, encoder)
    with h5py.File(args.output_file, 'w') as outf:
        new_agent.serialize(outf)

if __name__ == '__main__':
    main()