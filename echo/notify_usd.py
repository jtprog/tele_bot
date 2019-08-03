from telegram import Bot

from apis.cbrf import get_rate
from echo.config import load_config


NOTIFY_USER_ID = -1001386305123


def main():
    item = get_rate()
    if item:
        message = f'Курс {item.name} = {item.rate} руб.'
    else:
        message = 'Ошибка при поиске курса'

    config = load_config()
    bot = Bot(
        token=config.TG_TOKEN,
        base_url=config.TG_API_URL,
    )
    bot.send_message(
        chat_id=NOTIFY_USER_ID,
        text=message,
    )


if __name__ == '__main__':
    main()
