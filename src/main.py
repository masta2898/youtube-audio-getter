import os

import imageio

from src.bot import Bot

imageio.plugins.ffmpeg.download()

API_TOKEN = '731824033:AAGHUrLFC0cH-66SYksu8VkfanQ77wqkV7g'

# webhook settings
WEBHOOK_HOST = 'https://youtube-audio-getter.herokuapp.com'
WEBHOOK_PATH = '/webhook/'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# webserver settings
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = os.getenv('PORT')

if __name__ == '__main__':
    bot = Bot(API_TOKEN, WEBAPP_HOST, WEBAPP_PORT, WEBHOOK_HOST, WEBHOOK_PATH)
    bot.run()
