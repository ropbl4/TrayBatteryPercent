import psutil
import pystray
from PIL import Image
from time import sleep

import painting

# IMAGES_PATH = 'D:/img/'
# IMAGE_BATTERY_PATH = IMAGES_PATH + 'bat.ico'
# IMAGE_DIGITS_PATH = IMAGES_PATH + 'digits/digits.ico'

REFRESH_PAUSE_SEC = 5

MAIN_SIZE_X = painting.MAIN_SIZE_X
MAIN_SIZE_Y = painting.MAIN_SIZE_Y
DIGIT_SIZE_X = painting.DIGIT_SIZE_X
DIGIT_SIZE_Y = painting.DIGIT_SIZE_Y

INDENT_FIRST_NUMBER_X = 3
INDENT_FIRST_NUMBER_Y = 0
INDENT_BETWEEN_NUMBERS = 0
INDENT_BATTERY_Y = 9

ICO_RESOLUTION_MULTIPLIER = painting.ICO_RESOLUTION_MULTIPLIER

NO_BATTERY_TEXT = 'No Battery (are we on PC ?)'
NO_BAT = -1
BAT_FIRST_INIT = -2


def get_battery_percent() -> int:
    """ Возвращает текущий процент батареи (целое число). """

    # battery = psutil.sensors_battery()  # TODO: добавить статус подключённой зарядки ?
    # print(f'{battery = }')
    #
    # if battery is None:
    #     return NO_BAT
    #
    # battery_percent = battery.percent

    from random import randint

    # rand_category = 2
    rand_category = randint(0, 5)
    if rand_category == 0:
        battery_percent = NO_BAT
    elif rand_category == 1:
        battery_percent = 100
    elif rand_category == 2:
        battery_percent = randint(0, 9)
    elif rand_category == 3:
        battery_percent = randint(10, 19)
    else:
        battery_percent = randint(10, 99)  # for tests
    print(f'Random {battery_percent = }')

    # battery_percent = g_current_battery_percent - 1

    return battery_percent


# todo: если есть изображения цифр и батареи в определённой папке - по_CROP_ать их оттуда и заполнить список ими.
def get_from_image_img_digits_list() -> list[Image]:
    """ Вырезает цифры и батарею с изображений на диске,
        заполняет ими массив объектов PIL.Image. """

    pass


def get_img_digits_list() -> list[Image]:
    """ Возвращает список изображений с цифрами и батареей,
        полученный с картинок или, если их нет, нарисованный. """

    if False:  # если найдена папка /img/ и в ней есть картинка с цифрами и батареей...
        return get_from_image_img_digits_list()
    else:
        return painting.create_img_digits_list()


def change_percent_on_image(img_main: Image, img: list[Image], bat_perc: int | None) -> Image:
    """ Вставляет на значок изображения с нужными цифрами и батареей в правильные места. """

    print('I refresh %')
    # если нет батареи (мы на PC):
    if bat_perc == NO_BAT:
        return img[20]

    digit_size_x = DIGIT_SIZE_X
    ifx = INDENT_FIRST_NUMBER_X
    ify = INDENT_FIRST_NUMBER_Y
    ibn = INDENT_BETWEEN_NUMBERS
    iby = INDENT_BATTERY_Y
    rm = ICO_RESOLUTION_MULTIPLIER
    prev_bat = g_previous_battery_percent

    n_tens = bat_perc // 10
    n_prev = prev_bat // 10

    # если кол-во цифр в числе меняется (и это не первый вывод числа) - ...
    # ... очищаем значок от предыдущих цифр прозрачным прямоугольником:
    if n_tens != n_prev and prev_bat != BAT_FIRST_INIT:
        img_main.paste(im='#00000000', box=(0, 0, MAIN_SIZE_X * rm, DIGIT_SIZE_Y * rm))

    # располагаем цифры на значок в нужные места:
    if bat_perc == 100:
        img_main.paste(im=img[1], box=(0 * rm, ify * rm))
        img_main.paste(im=img[0], box=(5 * rm, ify * rm))
        img_main.paste(im=img[0], box=(10 * rm, ify * rm))
        n_bat = 19
    elif bat_perc < 10:
        img_main.paste(im=img[bat_perc], box=(5 * rm, ify * rm))
        n_bat = 10
    else:
        n_ones = bat_perc % 10
        n_bat = n_tens + 10

        if n_tens == 1:
            ifx -= 1

        if n_tens != n_prev:
            img_main.paste(im=img[n_tens], box=(ifx * rm, ify * rm))
        img_main.paste(im=img[n_ones], box=((ifx + digit_size_x + ibn) * rm, ify * rm))

    if n_tens != n_prev:
        # располагаем рисунок батареи на значок:
        img_main.paste(im=img[n_bat], box=(0, iby * rm))

    return img_main


def on_refresh_item(tray):
    """ Принудительное обновление изображения значка (даже если % совпадает). """

    battery_percent = get_battery_percent()

    tray.icon = change_percent_on_image(img_tray_ico, img_digits_list, battery_percent)
    tray.title = str(battery_percent) + '%' if battery_percent != NO_BAT else NO_BATTERY_TEXT

    global g_previous_battery_percent
    g_previous_battery_percent = battery_percent


def on_exit_item(tray):
    """ Обработчик пункта меню Exit (завершает программу). """

    tray.stop()

    global g_stop
    g_stop = True


def auto_check_battery_percent(tray) -> None:
    """ Авто-проверка процента батареи (в отдельном потоке средствами pystray). """

    global g_previous_battery_percent

    tray.visible = True

    for _ in range(1000000000):
        if g_stop:
            break

        battery_percent = get_battery_percent()

        if battery_percent != g_previous_battery_percent:
            tray.icon = change_percent_on_image(img_tray_ico, img_digits_list, battery_percent)
            tray.title = str(battery_percent) + '%' if battery_percent != NO_BAT else NO_BATTERY_TEXT
            g_previous_battery_percent = battery_percent

        sleep(REFRESH_PAUSE_SEC)
        print(f'{_ = } | ', end='')


def main():
    """ Создаёт объект значка в трее с изображением и меню. """

    battery_percent = get_battery_percent()

    tray_ico = change_percent_on_image(img_tray_ico, img_digits_list, battery_percent)
    tray_title = str(battery_percent) + '%' if battery_percent != NO_BAT else NO_BATTERY_TEXT
    tray_menu = pystray.Menu(pystray.MenuItem(text='Refresh % !', action=on_refresh_item, default=True),
                             pystray.MenuItem(text='Exit !', action=on_exit_item))
    tray = pystray.Icon(name='Battery Percent', icon=tray_ico, title=tray_title, menu=tray_menu)

    tray.SETUP_THREAD_TIMEOUT = 0

    global g_previous_battery_percent
    g_previous_battery_percent = battery_percent

    tray.run(setup=auto_check_battery_percent)
    # tray.run()


if __name__ == '__main__':
    g_previous_battery_percent = BAT_FIRST_INIT
    g_stop = False
    img_tray_ico = Image.new(mode='RGBA',
                             size=(MAIN_SIZE_X * ICO_RESOLUTION_MULTIPLIER, MAIN_SIZE_Y * ICO_RESOLUTION_MULTIPLIER),
                             color=(0, 0, 0, 0))
    img_digits_list = get_img_digits_list()

    main()

# todo: less PAUSE_SEC if < 21%
# todo: light theme
# todo: many screen resolutions...
