import inspect
import logging
from typing import List

from telegram import Update, Bot as TelegramBot, MessageEntity
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from src.audio_file import AudioFile
from src.user_session import UserSession
from src.youtube_audio_getter import YoutubeAudioGetter


class Bot:
    def __init__(self, token):
        self.updater = Updater(token, request_kwargs={'read_timeout': 120, 'connect_timeout': 120})
        self.dispatcher = self.updater.dispatcher

        self.__handlers = {
            self.__start: 'start',
            self.__stop: 'stop',
            self.__help: 'help',
            self.__echo: 'echo',
            self.__set_time: 'time',
        }

        self.__sessions: {int: UserSession} = dict()

    def run(self):
        logging.basicConfig(level=logging.DEBUG)
        self.__register_commands()
        self.updater.start_polling()
        self.updater.idle()

    def __register_commands(self):
        for handler, command in self.__handlers.items():
            self.dispatcher.add_handler(CommandHandler(command, handler))
        self.dispatcher.add_handler(MessageHandler(Filters.text, self.__get_audio))

    def __start(self, bot: TelegramBot, update: Update):
        chat_id = update.message.chat.id
        if chat_id in self.__sessions:
            del self.__sessions[chat_id]
            self.__sessions[chat_id] = UserSession(chat_id)
        update.message.chat.send_message("Hey! Use /help to get list of commands. Send url to download audio.")

    def __stop(self, bot: TelegramBot, update: Update):
        chat_id = update.message.chat.id
        if chat_id in self.__sessions:
            del self.__sessions[chat_id]

    def __help(self, bot: TelegramBot, update: Update):
        """Get this help message."""
        help_text = str()
        for handler, command in self.__handlers.items():
            help_text += f"{command} - {inspect.getdoc(handler)}\n"

        if help_text:
            help_text = f"List of bot's commands:\n{help_text}"
            update.message.chat.send_message(help_text)

    def __echo(self, bot: TelegramBot, update: Update):
        """Repeats your message."""
        logging.info(update)
        text = update.message.text
        if text:
            update.message.chat.send_message(text)

    def __set_time(self, bot: TelegramBot, update: Update):
        """Set time in minutes to divide video to parts."""
        chat_id = update.message.chat.id
        time = update.message.text.split()
        logging.info(time)
        if len(time) != 2:
            return update.message.chat.send_message("Set time in seconds!")

        try:
            time = int(time[1])
        except ValueError:
            return update.message.chat.send_message("Invalid time!")

        if chat_id in self.__sessions:
            self.__sessions[chat_id].set_part_time(time)

    def __get_audio(self, bot: TelegramBot, update: Update):
        chat_id = update.message.chat.id
        if chat_id not in self.__sessions:
            self.__sessions[chat_id] = UserSession(chat_id)

        current_session: UserSession = self.__sessions[chat_id]
        audio_getter = YoutubeAudioGetter()
        part_time = current_session.get_part_time()
        if part_time > 0:
            audio_getter.set_part_len(part_time)
        current_session.set_audio_getter(audio_getter)

        url = None
        entities = update.message.entities
        if entities:
            if entities[0].type == MessageEntity.URL:
                url = update.message.parse_entity(entities[0])

        if not url:
            return update.message.chat.send_message("Send url!")

        audio_files: List[AudioFile] = current_session.get_audio(url)
        for audio_file in audio_files:
            with open(audio_file.get_filename(), 'rb') as file:
                result = update.message.chat.send_audio(file, caption=audio_file.get_name())
            logging.info(result)
