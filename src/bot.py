import inspect
import asyncio
import logging

from aiogram import Bot as AiogramBot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import start_webhook


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

    def __register_commands(self):
        for handler, commands in self.__handlers.items():
            self.dispatcher.register_message_handler(handler, commands=commands)

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
        pass
