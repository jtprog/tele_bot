from telegram import Bot
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import Updater
from telegram.ext import MessageHandler
from telegram.ext import Filters
from telegram.utils.request import Request


def log_errors(f):

    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            print(f'[ошибка]: {e}')
            raise e

    return inner


@log_errors
def message_handler(update: Update, context: CallbackContext):
    user = update.effective_user
    if user:
        name = user.first_name
    else:
        name = 'аноним'

    text = update.effective_message.text
    reply_text = f'Привет, {name}!\n\n{text}'

    update.message.reply_text(
        text=reply_text,
    )


def main():
    print('Start')

    req = Request(
        connect_timeout=0.5,
        read_timeout=1.0,
    )
    bot = Bot(
        token='855883347:AAHxvaX7DSchTqeXA59q3yqbQw74ZHixVM4',
        request=req,
    )
    updater = Updater(
        bot=bot,
        use_context=True,
    )

    # Проверить что бот корректно подключился к Telegram API
    info = bot.get_me()
    print(f'Bot info: {info}')

    # Навесить обработчики команд
    handler = MessageHandler(Filters.all, message_handler)
    updater.dispatcher.add_handler(handler)

    # Начать бесконечную обработку входящих сообщений
    updater.start_polling()
    updater.idle()
    print('Finish')


if __name__ == '__main__':
    main()
