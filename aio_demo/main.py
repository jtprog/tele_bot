import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.bot import api
import sentry_sdk
from sentry_sdk.integrations.aiohttp import AioHttpIntegration

sentry_sdk.init(
    dsn="https://5f433888d1724989ad4752e9e8a5b014@o412493.ingest.sentry.io/5289339",
    integrations=[AioHttpIntegration()]
)


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


# TODO: раскомментировать если у вас ошибка подключения к ``api.telegram.org``
# Подмена базового URL для запросов
# PATCHED_URL = "https://telegg.ru/orig/bot{token}/{method}"
# setattr(api, 'API_URL', PATCHED_URL)


# Создать глобального бота
bot = Bot(
    token='1024509476:AAEA6B9bpWxAl0Uqg25WZ3ByL7cQdvTusDw',
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
    try:
        text = message.text
        if text and not text.startswith('/'):
            # q = 1 / 0
            await message.reply(text=text)
    except Exception as e:
        sentry_sdk.capture_exception(error=e)


def main():
    executor.start_polling(
        dispatcher=dp,
    )


if __name__ == '__main__':
    main()
