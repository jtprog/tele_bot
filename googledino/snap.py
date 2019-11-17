import time

import mss
from PIL import Image
from PIL import ImageColor
from PIL import ImageDraw

from googledino.main import BOX_COORD


# Шаг сетки в пикселях
layout_step = 100

# Ширина линий сетки в пикселях
layout_width = 2


def get_filename():
    filename = 'snapshot_{}.png'.format(int(time.time()))
    return filename


def snapshot():
    """ Сделать скриншот экрана и нарисовать поверх сетку
    """
    # Проверить разрешение монитора для калибровки коэфициентов в коде.
    # Вот что выдаёт мне библиотека: {'left': 0, 'top': 0, 'width': 1440, 'height': 900}
    # А вот мой размер экрана на самом деле: X=2880, Y=1800
    sct = mss.mss()
    m = sct.monitors[0]
    print(m)

    # Сделать скриншот
    sct_img = sct.grab(m)

    # Create the Image
    img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")

    draw = ImageDraw.Draw(im=img, mode=img.mode)
    fill = ImageColor.getrgb('red')

    width, height = img.size
    print(f'Разрешение скриншота: X={width}, Y={height}')

    # Нарисовать вертикальные линии через каждые 100px
    for i in range(0, width, layout_step):
        draw.line(xy=((i, 0), (i, height)), fill=fill, width=layout_width)

    # Нарисовать горизонтальные линии через каждые 100px
    for i in range(0, height, layout_step):
        draw.line(xy=((0, i), (width, i)), fill=fill, width=layout_width)

    # Нарисовать пару координат
    draw.line(xy=((0, 0), (layout_step, layout_step)), fill=fill, width=layout_width)

    # Нарисовать коробку из MSS
    # FIXME: тут платформо-специфичный код.
    #  Для Mac OS с ретиной MSS неправильно вычисляет расширение: оно в два раза меньше реального
    outline = ImageColor.getrgb('green')

    for box in (BOX_COORD):
        box_xy = (
            (box['left'] * 2, box['top'] * 2, ),
            ((box['left'] + box['width']) * 2, (box['top'] + box['height']) * 2),
        )
        draw.rectangle(xy=box_xy, outline=outline, width=6)

    img.save(get_filename())
    print('Экран размечен!')


if __name__ == '__main__':
    snapshot()
