import logging.config
import os

import sentry_sdk


# Путь до коренной папки `tele_bot`
BASE_PATH = os.path.dirname(os.path.dirname(__file__))

# TODO: вписать сюда токен от своего бота!!!
TG_TOKEN = "1024509476:AAEA6B9bpWxAl0Uqg25WZ3ByL7cQdvTusDw"

# На сервере не используем прокси-URL
TG_API_URL = None

# Валютная пара для уведомления
NOTIFY_PAIR = "USD-BTC"
# ID чата для уведомлений о курсе BTC
NOTIFY_USER_ID = 3995137

# ID чата для уведомлений о курсе $
USD_NOTIFY_USER_ID = 3995137

# ID чата (владельца канала) для получения отзывов/заявок
FEEDBACK_USER_ID = 3995137

# Логирование
LOGGING = {
    'disable_existing_loggers': True,
    'version': 1,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(module)s.%(funcName)s | %(asctime)s | %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}
logging.config.dictConfig(LOGGING)

# Sentry
# TODO: добавить свой DSN из https://sentry.io
sentry_sdk.init("https://5f433888d1724989ad4752e9e8a5b014@o412493.ingest.sentry.io/5289339")
