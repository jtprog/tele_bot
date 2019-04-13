import time
import random

from PIL import Image
from PIL import ImageFont
from PIL import ImageColor
from PIL import ImageDraw


def main():
    image_mode = "RGB"
    image_size = (640, 480)
    image_color = "#0000ff"
    font_size = 48
    font_color = "#00ffff"

    # Создать новую виртуальную картинку:
    # - заданной цветовой палитры (mode)
    # - заданного размера (size)
    # - и заданного цвета (color)
    img = Image.new(mode=image_mode, size=image_size, color=image_color)

    # Загрузить шрифт и цвет для нанесения надписей
    font = ImageFont.truetype("MULLERBOLD.OTF", size=font_size)
    fill = ImageColor.getrgb(color=font_color)

    # Создать точку входа в "рисование"
    # Любые изменения в виртуальной картинке хранятся и управляются здесь
    draw = ImageDraw.Draw(im=img, mode=img.mode)

    # Рисование происходит относительно верхнего левого угла
    # Поэтому нужно вычислить размер текстового блока с учётом размера шрифта
    text = ["Успех!", "Очень длинная строка", "Цена: 5555 $", ]
    sorted_text = sorted(text, key=lambda i: len(i), reverse=True)
    longest_line = sorted_text[0]
    print("Вычисляем ширину блока исходя из `{}`".format(longest_line))

    text_width, text_height = font.getsize(longest_line)
    text_height *= len(text)
    real_text = "\n".join(text)

    # Нанести текст так, чтобы он оказался ровно по центру картинки
    x = image_size[0] / 2 - text_width / 2
    y = image_size[1] / 2 - text_height / 2
    draw.text(xy=(x, y), text=real_text, fill=fill, font=font, align="center")

    draw.point(xy=(x, y))

    # Сохранить получившуюся картинку в файл на компьютере
    # (Однако, чтобы отправить картинку по сети, сохранять в файл не обязательно)
    filename = "result_{}_{}.png".format(int(time.time()), random.randint(1, 100))
    print("Сохраняю в файл `{}`".format(filename))
    img.save(filename)


if __name__ == '__main__':
    main()
