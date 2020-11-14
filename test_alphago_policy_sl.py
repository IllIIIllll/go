# © 2020 지성. all rights reserved.
# <llllllllll@kakao.com>
# MIT License

from dlgo.data.processor import GoDataProcessor
from dlgo.encoders.alphago import AlphaGoEncoder
from dlgo.networks.alphago import alphago_model

rows, cols = 19, 19
num_classes = rows * cols
num_games = 10000

encoder = AlphaGoEncoder()
processor = GoDataProcessor(encoder=encoder.name())
generator = processor.load_go_data('train', num_games, use_generator=True)
test_generator = processor.load_go_data('test', num_games, use_generator=True)

input_shape = (encoder.num_planes, rows, cols)
alphago_sl_policy = alphago_model(input_shape, is_policy_net=True)

alphago_sl_policy.compile('sgd', 'categorical_crossentropy', metrics=['accuracy'])