import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.bot import api


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


# TODO: раскомментировать если у вас ошибка подключения к ``api.telegram.org``
# Подмена базового URL для запросов
# PATCHED_URL = "https://telegg.ru/orig/bot{token}/{method}"
# setattr(api, 'API_URL', PATCHED_URL)


# Создать глобального бота
bot = Bot(
    token='XXX',
)
dp = Dispatcher(
    bot=bot,
)


@dp.message_handler(commands=['help', 'help2'])
async def send_menu(message: types.Message):
    """ Отправить список команд бота
    """
    await message.reply(
        text='''
Мои команды:
/help -- увидеть это сообщение

бла бла
''',
        reply=False,
    )


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    # Поприветствовать
    await message.reply("Привет!\nЯ - EchoBot!")
    # Показать список команд
    await send_menu(message=message)


@dp.message_handler(content_types=types.ContentType.TEXT)
async def do_echo(message: types.Message):
    text = message.text
    if text and not text.startswith('/'):
        await message.reply(text=text)


def main():
    executor.start_polling(
        dispatcher=dp,
    )


if __name__ == '__main__':
    main()
