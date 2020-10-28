# © 2020 지성. all rights reserved.
# <llllllllll@kakao.com>
# MIT License

# http://127.0.0.1:5000/static/play_pg_99.html

import h5py

from dlgo.agent.pg import load_policy_agent
from dlgo.httpfrontend import get_web_app

model_file = h5py.File('../agents/pg_bot.h5')
bot_from_file = load_policy_agent(model_file)

web_app = get_web_app({'predict': bot_from_file})
web_app.run()