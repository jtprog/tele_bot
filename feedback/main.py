from logging import getLogger

from telegram import Bot
from telegram import Update
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters
from telegram.ext import Updater

from echo.config import load_config
from echo.utils import debug_requests


config = load_config()

logger = getLogger(__name__)


@debug_requests
def do_start(bot: Bot, update: Update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text='Отправь мне текст, и я перешлю его автору канала',
    )


@debug_requests
def do_echo(bot: Bot, update: Update):
    chat_id = update.message.chat_id

    if chat_id == config.FEEDBACK_USER_ID:
        # Смотрим на реплаи
        error_message = None
        reply = update.message.reply_to_message
        if reply:
            forward_from = reply.forward_from
            if forward_from:
                text = 'Сообщение от автора канала:\n\n' + update.message.text
                bot.send_message(
                    chat_id=forward_from.id,
                    text=text,
                )
            else:
                error_message = 'Нельзя ответить самому себе'
        else:
            error_message = 'Сделайте reply чтобы ответить автору сообщения'

        # Отправить сообщение об ошибке если оно есть
        if error_message is not None:
            bot.send_message(
                chat_id=chat_id,
                text=error_message,
            )
    else:
        # Пересылать всё как есть
        bot.forward_message(
            chat_id=config.FEEDBACK_USER_ID,
            from_chat_id=update.message.chat_id,
            message_id=update.message.message_id,
        )
        bot.send_message(
            chat_id=chat_id,
            text='Сообщение было отправлено',
        )


def main():
    logger.info('Запускаем бота...')

    bot = Bot(
        token=config.TG_TOKEN,
        base_url=config.TG_API_URL,
    )
    updater = Updater(
        bot=bot,
    )

    start_handler = CommandHandler('start', do_start)
    message_handler = MessageHandler(Filters.all, do_echo)
    updater.dispatcher.add_handler(start_handler)
    updater.dispatcher.add_handler(message_handler)

    # Начать обработку входящих сообщений
    updater.start_polling()
    # Не прерывать скрипт до обработки всех сообщений
    updater.idle()

    logger.info('Закончили...')


if __name__ == '__main__':
    main()
