import random
import time
import os
from logging import getLogger
from io import BytesIO

from PIL import Image


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
    return filename


def debug_requests(f):
    """ Декоратор для отладки событий от телеграма
        Логгер подключается в самый последний момент чтобы быть уверенными в том, что конфиг логирования уже загружен
    """
    from logging import getLogger
    logger = getLogger(__name__)

    def inner(*args, **kwargs):
        try:
            logger.debug('Обращение в функцию {}'.format(f.__name__))
            return f(*args, **kwargs)
        except Exception:
            logger.exception('Ошибка в обработчике {}'.format(f.__name__))
            raise

    return inner


def save_image(img: Image, img_format=None, quality=85):
    """ Сохранить картинку из потока в переменную для дальнейшей отправки по сети
    """
    if img_format is None:
        img_format = img.format
    output_stream = BytesIO()
    output_stream.name = 'image.jpeg'
    # на Ubuntu почему-то нет jpg, но есть jpeg
    if img.format == 'JPEG':
        img.save(output_stream, img_format, quality=quality, optimize=True, progressive=True)
    else:
        img.convert('RGB').save(output_stream, format=img_format)
    output_stream.seek(0)
    return output_stream
