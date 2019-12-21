from logging import getLogger

from telegram import InlineQueryResultArticle
from telegram import InputTextMessageContent
from telegram import ReplyKeyboardRemove
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import Filters
from telegram.ext import InlineQueryHandler
from telegram.ext import MessageHandler
from telegram.ext import Updater

from echo.config import load_config
from echo.utils import debug_requests
from inline.search import Searcher


config = load_config()
logger = getLogger(__name__)

search = Searcher()


@debug_requests
def echo_handler(update: Update, context: CallbackContext):
    if not update.message:
        return
    update.message.reply_text(
        text=f'В личке бота ничего нет. Перейтиде в любой другой диалог и начните печатать юзернейм бота: @{update.message.bot.username}',
        reply_markup=ReplyKeyboardRemove(),
    )


@debug_requests
def inline_handler(update: Update, context: CallbackContext):
    query = update.inline_query.query
    query = query.strip().lower()
    logger.info('inline: %s', query)

    # Список похожих имён монет
    results = []
    names = search.parse_query(text=query)
    prices = search.get_prices(names=names)
    for i, (name, price) in enumerate(prices):
        results.append(
            InlineQueryResultArticle(
                id=i + 1,
                title=f'{name} now?',
                input_message_content=InputTextMessageContent(
                    message_text=f'{name} is {price}$ now!',
                ),
            )
        )

    # Ничего не нашлось
    if query and not results:
        results.append(
            InlineQueryResultArticle(
                id=999,
                title='Ничего не нашлось',
                input_message_content=InputTextMessageContent(
                    message_text=f'Ничего не нашлось по запросу "{query}"',
                ),
            )
        )

    update.inline_query.answer(
        results=results,
        cache_time=10,
    )


def main():
    # Создать бота
    logger.info('Start bot')

    updater = Updater(
        token='855883347:AAH9ikaPCy1R2GoqbhmCGilhFmqLczcUFAY',
        base_url='https://telegg.ru/orig/bot',
        use_context=True,
    )
    # Загрузить информацию о боте
    logger.info(updater.bot.get_me())

    updater.dispatcher.add_handler(MessageHandler(filters=Filters.text, callback=echo_handler))
    updater.dispatcher.add_handler(InlineQueryHandler(inline_handler))

    updater.start_polling()
    updater.idle()

    logger.info('Finish bot')


if __name__ == '__main__':
    main()
