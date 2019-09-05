from logging import getLogger

from telegram import Bot
from telegram import Update
from telegram import ReplyKeyboardRemove
from telegram.ext import Updater
from telegram.ext import MessageHandler
from telegram.ext import CommandHandler
from telegram.ext import ConversationHandler
from telegram.ext import Filters

from echo.config import load_config
from echo.utils import debug_requests
from anketa.validators import GENDER_MAP
from anketa.validators import gender_hru
from anketa.validators import validate_age
from anketa.validators import validate_gender


config = load_config()

logger = getLogger(__name__)


NAME, GENDER, AGE = range(3)


@debug_requests
def start_handler(bot: Bot, update: Update):
    # Спросить имя
    update.message.reply_text(
        'Введи своё имя чтобы продолжить:',
        reply_markup=ReplyKeyboardRemove(),
    )
    return NAME


@debug_requests
def name_handler(bot: Bot, update: Update, user_data: dict):
    # Получить имя
    user_data[NAME] = update.message.text
    logger.info('user_data: %s', user_data)

    # Спросить пол
    genders = [f'{key} - {value}' for key, value in GENDER_MAP.items()]
    genders = '\n'.join(genders)
    update.message.reply_text(f'''
Выберите свой пол чтобы продолжить:
{genders}
''')
    # TODO: кнопки !
    return GENDER


@debug_requests
def age_handler(bot: Bot, update: Update, user_data: dict):
    # Получить пол
    gender = validate_gender(text=update.message.text)
    if gender is None:
        update.message.reply_text('Пожалуйста, укажите корректный пол!')
        return GENDER

    user_data[GENDER] = gender
    logger.info('user_data: %s', user_data)

    # Спросить возраст
    update.message.reply_text('''
Введите свой возраст:
''')
    return AGE


@debug_requests
def finish_handler(bot: Bot, update: Update, user_data: dict):
    # Получить возраст
    age = validate_age(text=update.message.text)
    if age is None:
        update.message.reply_text('Пожалуйста, введите корректный возраст!')
        return AGE

    user_data[AGE] = age
    logger.info('user_data: %s', user_data)

    # TODO: вот тут запись в базу финала
    # TODO 2: очистить `user_data`

    # Завершить диалог
    update.message.reply_text(f'''
Все данные успешно сохранены! 
Вы: {user_data[NAME]}, пол: {gender_hru(user_data[GENDER])}, возраст: {user_data[AGE]} 
''')
    return ConversationHandler.END


@debug_requests
def cancel_handler(bot: Bot, update: Update):
    """ Отменить весь процесс диалога. Данные будут утеряны
    """
    update.message.reply_text('Отмена. Для начала с нуля нажмите /start')
    return ConversationHandler.END


@debug_requests
def echo_handler(bot: Bot, update: Update):
    update.message.reply_text(
        'Нажмите /start для заполнения анкеты!',
        reply_markup=ReplyKeyboardRemove(),
    )


def main():
    logger.info('Start bot')
    bot = Bot(
        token=config.TG_TOKEN,
        base_url=config.TG_API_URL,
    )
    updater = Updater(
        bot=bot,
    )

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('start', start_handler),
        ],
        states={
            NAME: [
                MessageHandler(Filters.all, name_handler, pass_user_data=True),
            ],
            GENDER: [
                MessageHandler(Filters.all, age_handler, pass_user_data=True),
            ],
            AGE: [
                MessageHandler(Filters.all, finish_handler, pass_user_data=True),
            ],
        },
        fallbacks=[
            CommandHandler('cancel', cancel_handler),
        ],
    )
    updater.dispatcher.add_handler(conv_handler)
    updater.dispatcher.add_handler(MessageHandler(Filters.all, echo_handler))

    updater.start_polling()
    updater.idle()
    logger.info('Finish bot')


if __name__ == '__main__':
    main()
