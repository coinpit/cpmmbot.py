#!/usr/bin/env python
import time
from pymmbot import mmbot
from pymmbot.utils import common_util

bot = mmbot.MMBot()
bot.connect()
time.sleep(10)
bot.initiate()
common_util.loop()
