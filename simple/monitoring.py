import logging

import sentry_sdk


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


# TODO: добавить свой DSN из https://sentry.io
sentry_sdk.init(
    dsn=None,
    debug=True,
)

try:
    # division_by_zero = 1 / 0
    raise Exception('xxx')
except Exception as e:
    sentry_sdk.capture_exception(error=e)
    raise
