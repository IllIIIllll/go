# © 2020 지성. all rights reserved.
# <llllllllll@kakao.com>
# MIT License

# http://127.0.0.1:5000/static/play_predict_19.html

import h5py

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

from dlgo.agent.predict import DeepLearningAgent, load_prediction_agent
from dlgo.data.processor import GoDataProcessor
from dlgo.encoders.sevenplane import SevenPlaneEncoder
from dlgo.httpfrontend import get_web_app
from dlgo.networks import large

go_board_rows, go_board_cols = 19, 19
nb_classes = go_board_rows * go_board_cols
encoder = SevenPlaneEncoder((go_board_rows, go_board_cols))
processor = GoDataProcessor(encoder=encoder.name())

X, y = processor.load_go_data(num_samples=100)

input_shape = (encoder.num_planes, go_board_rows, go_board_cols)
model = Sequential()
network_layers = large.layers(input_shape)
for layer in network_layers:
    model.add(layer)
model.add(Dense(nb_classes, activation='softmax'))
model.compile(
    loss='categorical_crossentropy',
    optimizer='adadelta',
    metrics=['accuracy']
)
model.fit(X, y, batch_size=128, epochs=20, verbose=1)

deep_learning_bot = DeepLearningAgent(model, encoder)
deep_learning_bot.serialize('../agents/deep_bot.h5')

model_file = h5py.File('../agents/deep_bot.h5')
bot_from_file = load_prediction_agent(model_file)

web_app = get_web_app({'predict': bot_from_file})
web_app.run()