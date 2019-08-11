import random
import time
import os
from logging import getLogger


logger = getLogger(__name__)


def mkdir(path):
    """ Создать новую папку или убедиться что она уже существует

    :param str path: желаеный путь до новой папки
    """
    if os.path.exists(path):
        return True
    elif os.path.isfile(path):
        return False
    try:
        os.mkdir(path=path)
        return True
    except FileExistsError:
        return False


def get_filename():
    filename = 'result_{}_{}.png'.format(int(time.time()), random.randint(1, 100))
    logger.debug('Сохраняю в файл `%s`', filename)
    return filename


def debug_requests(f):
    """ Декоратор для отладки событий от телеграма
    """
    def inner(*args, **kwargs):
        try:
            logger.info('Обращение в функцию {}'.format(f.__name__))
            return f(*args, **kwargs)
        except Exception:
            logger.exception('Ошибка в обработчике {}'.format(f.__name__))
            raise

    return inner
