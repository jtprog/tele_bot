from telegram import Bot
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import Updater
from telegram.utils.request import Request


TOKEN = '...'

PROXY_URL = 'https://telegg.ru/orig/bot'

ADMIN_IDS = [
    123,
    50512389,
]

# Ваш ID
MAIN_ADMIN_ID = 50512389


def do_echo(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    text = update.message.text

    reply_text = "Ваш ID = {}\n\n{}".format(chat_id, text)
    update.message.reply_text(
        text=reply_text,
    )


def admin_access(f):

    def inner(*args, **kwargs):
        update = args[0]
        if update and hasattr(update, 'message'):
            chat_id = update.message.chat_id
            if chat_id in ADMIN_IDS:
                print('Доступ разрешен!')
                return f(*args, **kwargs)
            else:
                print('Доступ не разрешен!')
        else:
            print('Нет агрумента update')

    return inner


def log_errors(f):

    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            error_message = f'[ADMIN] Произошла ошибка: {e}'
            print(error_message)

            update = args[0]
            if update and hasattr(update, 'message'):
                # Сообщение о любой ошибке всегда отправляется главному админу
                update.message.bot.send_message(
                    chat_id=MAIN_ADMIN_ID,
                    text=error_message,
                )

                # Отправлять сообщение об ошибке только если она произошла у вас
                # chat_id = update.message.chat_id
                # if chat_id in ADMIN_IDS:
                #     update.message.reply_text(
                #         text=error_message,
                #     )

            raise e

    return inner


@admin_access
@log_errors
def secret_command(update: Update, context: CallbackContext):
    update.message.reply_text(
        text='секрет!',
    )


@log_errors
def secret_command2(update: Update, context: CallbackContext):
    # Специальная функция с ошибкой чтобы отлаживать работу логирования
    update.xxxx.reply_text(
        text='секрет 222!',
    )


def main():
    # 1 -- правильное подключение
    request = Request(
        connect_timeout=0.5,
        read_timeout=1.0,
    )
    bot = Bot(
        request=request,
        token=TOKEN,
        base_url=PROXY_URL,
    )
    print(bot.get_me())

    # 2 -- обработчики
    updater = Updater(
        bot=bot,
        use_context=True,
    )

    message_handler = MessageHandler(Filters.text, do_echo)
    updater.dispatcher.add_handler(message_handler)

    command1 = CommandHandler('secret', secret_command)
    updater.dispatcher.add_handler(command1)

    command2 = CommandHandler('secret2', secret_command2)
    updater.dispatcher.add_handler(command2)

    # 3 -- запустить бесконечную обработку входящих сообщений
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
