import psutil
import pystray
from PIL import Image
from time import sleep
import winreg

import painting

# IMAGES_PATH = 'D:/img/'
# IMAGE_BATTERY_PATH = IMAGES_PATH + 'bat.ico'
# IMAGE_DIGITS_PATH = IMAGES_PATH + 'digits/digits.ico'

REFRESH_PAUSE_SEC_HIGH = 1
REFRESH_PAUSE_SEC_lOW = 1
PERCENT_LOW = 20
PERCENT_LOWEST = 10

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


def get_battery_percent() -> tuple[int, bool]:
    """ Возвращает текущий процент батареи (целое число). """

    # battery = psutil.sensors_battery()
    # print(f'{battery = }')
    #
    # if battery is None:
    #     return NO_BAT, False
    #
    # battery_percent = battery.percent
    # charging = battery.power_plugged

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

    rand_charge = randint(1, 3)
    charging = False if rand_charge <= 2 else True

    print(f'Random {battery_percent = }, {charging = }')

    # battery_percent = g_current_battery_percent - 1
    # battery_percent = 50
    # charging = False

    return battery_percent, charging


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


def is_theme_light() -> bool:
    """ Проверяет, светлая тема или тёмная (через параметр в реестре). """

    reg_path_hkey = winreg.HKEY_CURRENT_USER
    reg_path_folder = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize'

    try:
        with winreg.OpenKey(reg_path_hkey, reg_path_folder) as reg_key:
            print(f'{reg_path_hkey = }, {reg_key = }')
            light_theme = winreg.QueryValueEx(reg_key, 'SystemUsesLightTheme')

        return bool(light_theme[0])

    except FileNotFoundError:
        print('Key or value not found in registry.')

    return False


def change_tray_ico(img_main: Image, img: list[Image], bat_perc: int, charging: bool, light_theme: bool) -> Image:
    """ Вставляет на значок Image-объекты с нужными цифрами и батареей в правильные места и нужного цвета. """

    print('I refresh %', end=' | ')
    # если нет батареи (мы на PC):
    if bat_perc == NO_BAT:
        return img[20]

    digit_size_x = DIGIT_SIZE_X
    ifx = INDENT_FIRST_NUMBER_X
    ify = INDENT_FIRST_NUMBER_Y
    ibn = INDENT_BETWEEN_NUMBERS
    iby = INDENT_BATTERY_Y
    rm = ICO_RESOLUTION_MULTIPLIER
    # prev_bat = g_previous_battery_percent

    # n_prev = prev_bat // 10

    if charging:
        color = (0, 255, 0, 255)        # green (light + dark, low + high, plug)
    elif bat_perc <= PERCENT_LOWEST:
        color = (255, 0, 0, 255)        # red (light + dark, lowest, no_plug)
    elif bat_perc <= PERCENT_LOW:
        color = (255, 255, 0, 255)      # yellow (light + dark, low, no_plug)
    elif light_theme:
        color = (0, 0, 0, 255)          # black (light, high, no_plug)
    else:
        color = (255, 255, 255, 255)    # white (dark, high, no_plug)

    # import random
    # color = random.choice((
    #     # (255, 255, 255, 255),   # white (dark, high, no_plug)
    #     # (0, 0, 0, 255),         # black (light, high, no_plug)
    #     # (0, 255, 0, 255),       # green (light + dark, low + high, plug)
    #     (255, 0, 0, 255),       # red
    #     # (255, 255, 0, 255),     # yellow
    #     # (255, 50, 0, 255),      #
    #     # (255, 100, 0, 255),     #
    #     # (255, 150, 0, 255),     #
    #     # (255, 200, 0, 255),     #
    # ))
    print(f'{color = }')

    # если кол-во цифр в числе меняется (и это не первый вывод числа) - ...
    # ... очищаем значок от предыдущих цифр прозрачным прямоугольником:
    # if n_tens != n_prev and prev_bat != BAT_FIRST_INIT:
    img_main.paste(im='#00000000', box=(0, 0, MAIN_SIZE_X * rm, MAIN_SIZE_Y * rm))
        # img_main.paste(im='#00000000', box=(0, 0, MAIN_SIZE_X * rm, DIGIT_SIZE_Y * rm))
        # img_main.show()

    # располагаем цифры на значок в нужные места:
    if bat_perc == 100:
        img_main.paste(im=color, box=(0 * rm, ify * rm), mask=img[1])
        img_main.paste(im=color, box=(5 * rm, ify * rm), mask=img[0])
        img_main.paste(im=color, box=(10 * rm, ify * rm), mask=img[0])
        n_bat = 19
    elif bat_perc < 10:
        img_main.paste(im=color, box=(5 * rm, ify * rm), mask=img[bat_perc])
        n_bat = 10
    else:
        n_tens = bat_perc // 10
        n_ones = bat_perc % 10
        n_bat = n_tens + 10

        if n_tens == 1:
            ifx -= 1

        # if n_tens != n_prev:
        img_main.paste(im=color, box=(ifx * rm, ify * rm), mask=img[n_tens])
        img_main.paste(im=color, box=((ifx + digit_size_x + ibn) * rm, ify * rm), mask=img[n_ones])

    # if n_tens != n_prev:
        # располагаем рисунок батареи на значок:
    img_main.paste(im=color, box=(0, iby * rm), mask=img[n_bat])

    return img_main


def on_refresh_item(tray):
    """ Принудительное обновление изображения значка (даже если % совпадает). """

    battery_percent, charging = get_battery_percent()
    light_theme = is_theme_light()

    tray.icon = change_tray_ico(img_tray_ico, img_digits_list, battery_percent, charging, light_theme)
    tray.title = str(battery_percent) + '%' if battery_percent != NO_BAT else NO_BATTERY_TEXT

    global g_prev_bat_percent, g_prev_charging, g_prev_light_theme
    g_prev_bat_percent = battery_percent
    g_prev_charging = charging
    g_prev_light_theme = light_theme


def on_exit_item(tray):
    """ Обработчик пункта меню Exit (завершает программу). """

    tray.stop()

    global g_stop
    g_stop = True


def auto_check_battery_percent(tray) -> None:
    """ Авто-проверка процента батареи (в отдельном потоке средствами pystray). """

    global g_prev_bat_percent, g_prev_charging, g_prev_light_theme

    tray.visible = True

    for _ in range(1000000000):
        if g_stop:
            break

        battery_percent, charging = get_battery_percent()
        light_theme = is_theme_light()

        if battery_percent != g_prev_bat_percent or charging != g_prev_charging or light_theme != g_prev_light_theme:
            tray.icon = change_tray_ico(img_tray_ico, img_digits_list, battery_percent, charging, light_theme)
            tray.title = str(battery_percent) + '%' if battery_percent != NO_BAT else NO_BATTERY_TEXT

            g_prev_bat_percent = battery_percent
            g_prev_charging = charging
            g_prev_light_theme = light_theme

        if battery_percent > PERCENT_LOW + 1:
            sleep(REFRESH_PAUSE_SEC_HIGH)
        else:
            sleep(REFRESH_PAUSE_SEC_lOW)
        print(f'{_ = } | ', end='')


def main():
    """ Создаёт объект значка в трее с изображением и меню. """

    battery_percent, charging = get_battery_percent()
    light_theme = is_theme_light()

    tray_ico = change_tray_ico(img_tray_ico, img_digits_list, battery_percent, charging, light_theme)
    tray_title = str(battery_percent) + '%' if battery_percent != NO_BAT else NO_BATTERY_TEXT
    tray_menu = pystray.Menu(pystray.MenuItem(text='Refresh % !', action=on_refresh_item, default=True),
                             pystray.MenuItem(text='Exit !', action=on_exit_item))
    tray = pystray.Icon(name='Battery Percent', icon=tray_ico, title=tray_title, menu=tray_menu)

    tray.SETUP_THREAD_TIMEOUT = 0

    global g_prev_bat_percent, g_prev_charging, g_prev_light_theme
    g_prev_bat_percent = battery_percent
    g_prev_charging = charging
    g_prev_light_theme = light_theme

    tray.run(setup=auto_check_battery_percent)
    # tray.run()


if __name__ == '__main__':
    g_prev_bat_percent = BAT_FIRST_INIT
    g_prev_charging = BAT_FIRST_INIT
    g_prev_light_theme = None
    g_stop = False
    img_tray_ico = Image.new(mode='RGBA',
                             size=(MAIN_SIZE_X * ICO_RESOLUTION_MULTIPLIER, MAIN_SIZE_Y * ICO_RESOLUTION_MULTIPLIER),
                             color=(0, 0, 0, 0))
    img_digits_list = get_img_digits_list()

    main()

# todo: many screen resolutions...
