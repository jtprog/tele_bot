import time

import mss
import numpy as np
import cv2
import pyautogui as pg


BOX_COORD = {'top': 253 + 25, 'left': 275, 'width': 50, 'height': 80 - 25}


def process_image(original_image):
    # Создать копию входящей картинки в оттенках серого
    processed_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    # Найти границы всех объектов на картинке.
    # Используется алгоритм https://ru.wikipedia.org/wiki/Оператор_Кэнни
    processed_image = cv2.Canny(processed_image, threshold1=200, threshold2=300)
    return processed_image


def screen_record():
    # Подготовить класс для снятия скриншотов
    sct = mss.mss()
    last_time = time.time()

    while True:
        # Проверить нижнюю область.
        # Сделать скриншот заданной области экрана (прямоугольник перед персонажем)
        img = sct.grab(BOX_COORD)
        img = np.array(img)
        processed_image = process_image(img)

        # Посчитать среднее арифметическое всех границ. Если это значение отличается от 0,
        # то на нашей картинке есть препятствие. А значит его нужно перепрыгнуть.
        mean = np.mean(processed_image)
        print('down mean = ', mean)

        if mean != float(0):
            pg.press('space')

        print('loop took {} seconds'.format(time.time() - last_time))
        last_time = time.time()


if __name__ == '__main__':
    screen_record()
