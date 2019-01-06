import inspect
import asyncio
import logging
from typing import List

from aiogram import Bot as AiogramBot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import start_webhook

from src.audio_file import AudioFile
from src.user_session import UserSession
from src.youtube_audio_getter import YoutubeAudioGetter


class Bot:
    def __init__(self, token, host, port, webhook_host, webhook_path):
        self.token = token
        self.host = host
        self.port = port
        self.webhook_path = webhook_path
        self.webhook_url = f"{webhook_host}{webhook_path}"

        loop = asyncio.get_event_loop()
        self.bot = AiogramBot(token=token, loop=loop)
        self.dispatcher = Dispatcher(self.bot)

        self.__handlers = {
            self.__help: ['help'],
            self.__echo: ['echo', 'e'],
            self.__set_time: ['time', 't'],
        }

        self.__sessions: {int: UserSession} = dict()

    def run(self):
        logging.basicConfig(level=logging.DEBUG)
        start_webhook(dispatcher=self.dispatcher, webhook_path=self.webhook_path, on_startup=self.__on_startup,
                      on_shutdown=self.__on_shutdown, skip_updates=True, host=self.host, port=self.port)

    async def __on_startup(self, dispatcher):
        await self.bot.set_webhook(self.webhook_url)
        self.__register_commands()
        logging.info("Starting up.")

    async def __on_shutdown(self, dispatcher):
        logging.info("Shutting down.")

    async def __start(self, message: types.Message):
        user_id = message.chat.id
        if user_id in self.__sessions:
            del self.__sessions[user_id]
            self.__sessions[user_id] = UserSession(user_id)
        await self.bot.send_message(user_id, "Hey! Use /help to get list of commands. Send url to download audio.")

    async def __stop(self, message: types.Message):
        user_id = message.chat.id
        if user_id in self.__sessions:
            del self.__sessions[user_id]

    def __register_commands(self):
        for handler, commands in self.__handlers.items():
            self.dispatcher.register_message_handler(handler, commands=commands)
        self.dispatcher.register_message_handler(self.__get_audio, self.__is_url)

    def __is_url(self, message: types.Message):
        return message.entities[0].type == "url" if len(message.entities) == 1 else False

    async def __help(self, message: types.Message):
        """Get this help message."""
        help_text = str()
        for handler, commands in self.__handlers.items():
            help_text += " ".join(f"/{command}" for command in commands)
            help_text += f" - {inspect.getdoc(handler)}\n"

        if help_text:
            help_text = f"List of bot's commands:\n{help_text}"
            await self.bot.send_message(message.chat.id, help_text)

    async def __echo(self, message: types.Message):
        """Repeats your message."""
        text = message.get_args()
        if text:
            await self.bot.send_message(message.chat.id, text)

    async def __set_time(self, message: types.Message):
        """Set time in minutes to divide video to parts."""
        chat_id = message.chat.id
        time = message.get_args().split()
        if len(time) != 1:
            return await self.bot.send_message(chat_id, "Set time in seconds!")

        try:
            time = int(time[0])
        except ValueError:
            return await self.bot.send_message(chat_id, "Invalid time!")

        if chat_id in self.__sessions:
            self.__sessions[chat_id].set_part_time(time)

    async def __get_audio(self, message: types.Message):
        chat_id = message.chat.id
        if chat_id not in self.__sessions:
            self.__sessions[chat_id] = UserSession(chat_id)

        current_session: UserSession = self.__sessions[chat_id]
        audio_getter = YoutubeAudioGetter()
        part_time = current_session.get_part_time()
        if part_time > 0:
            audio_getter.set_part_len(part_time)
        current_session.set_audio_getter(audio_getter)

        url = message.entities[0].get_text(message.text)
        logging.info(f"Getting audio files from {url}")
        audio_files: List[AudioFile] = current_session.get_audio(url)
        for audio_file in audio_files:
            logging.info(f"Sending {audio_file.get_name()}")
            await self.bot.send_audio(chat_id, audio_file.get_data(), audio_file.get_name())
