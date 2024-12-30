import psutil
import pystray
from PIL import Image
from time import sleep
import winreg
import argparse

import painting

# IMAGES_PATH = 'D:/img/'
# IMAGE_BATTERY_PATH = IMAGES_PATH + 'bat.ico'
# IMAGE_DIGITS_PATH = IMAGES_PATH + 'digits/digits.ico'

REFRESH_PAUSE_SEC_HIGH = 2
REFRESH_PAUSE_SEC_lOW = 2
PERCENT_LOW = 20
PERCENT_LOWEST = 10

MAIN_SIZE_X = painting.MAIN_SIZE_X
MAIN_SIZE_Y = painting.MAIN_SIZE_Y
DIGIT_SIZE_X = painting.DIGIT_SIZE_X
DIGIT_SIZE_Y = painting.DIGIT_SIZE_Y

INDENT_FIRST_NUMBER_X = 3
INDENT_NUMBERS_Y = 0
INDENT_BETWEEN_NUMBERS = 0
INDENT_BATTERY_Y = 9

RM = painting.ICO_RESOLUTION_MULTIPLIER

NO_BATTERY_TEXT = 'No Battery (are we on PC ?)'
NO_BAT = -1


def get_battery_percent() -> tuple[int, bool]:
    """ Возвращает текущий процент батареи (целое число) и статус подключения зарядки (bool). """

    battery = psutil.sensors_battery()

    if battery is None:
        return NO_BAT, False

    battery_percent = battery.percent
    charging = battery.power_plugged

    return battery_percent, charging


def get_from_image_img_digits_list() -> list[Image]:
    """ Вырезает цифры и батарею с изображений на диске,
        заполняет ими массив объектов PIL.Image. """

    pass


def get_img_digits_list() -> list[Image]:
    """ Возвращает список изображений с цифрами и батареей,
        полученный с картинок или, если их нет, нарисованный. """

    if False:  # если найдена папка /img/ и в ней есть картинка с цифрами и батареей... Но я не стал это делать.
        return get_from_image_img_digits_list()
    else:
        return painting.create_img_digits_list()


def is_theme_light() -> bool:
    """ Проверяет, светлая тема или тёмная (через параметр в реестре). """

    reg_path_hkey = winreg.HKEY_CURRENT_USER
    reg_path_folder = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize'

    try:
        with winreg.OpenKey(reg_path_hkey, reg_path_folder) as reg_key:
            light_theme = winreg.QueryValueEx(reg_key, 'SystemUsesLightTheme')

        return bool(light_theme[0])

    except FileNotFoundError:
        # print('Key or value not found in registry.')
        pass

    return False


def get_color_and_bg(light_theme: bool, charging: bool, bat_perc: int) -> tuple:
    """ Получает цвета из параметров запуска скрипта (argparse).
        Возвращает картеж из 2-х цветов: цвет цифр с батареей и цвет фона.
        Оба цвета - картежи из 4-х целых чисел (red, green, blue, transparency). """
    
    if light_theme:
        if charging:
            color = g_args.light_charging_color if g_args.light_charging_color else (0, 255, 0, 255)  # green
            color_bg = g_args.light_charging_bg if g_args.light_charging_bg else (0, 0, 0, 255)       # black
        elif bat_perc <= PERCENT_LOWEST:
            color = g_args.light_lowest_color if g_args.light_lowest_color else (255, 0, 0, 255)      # red
            color_bg = g_args.light_lowest_bg if g_args.light_lowest_bg else (0, 0, 0, 255)
        elif bat_perc <= PERCENT_LOW:
            color = g_args.light_low_color if g_args.light_low_color else (255, 255, 0, 255)          # yellow
            color_bg = g_args.light_low_bg if g_args.light_low_bg else (0, 0, 0, 255)
        else:
            color = g_args.light_color if g_args.light_color else (0, 0, 0, 255)                      # black
            color_bg = g_args.light_bg if g_args.light_bg else (0, 0, 0, 0)                           # transparent
    else:                                                                                             # if dark theme:
        if charging:
            color = g_args.dark_charging_color if g_args.dark_charging_color else (0, 255, 0, 255)    # green
            color_bg = g_args.dark_charging_bg if g_args.dark_charging_bg else (0, 0, 0, 0)
        elif bat_perc <= PERCENT_LOWEST:
            color = g_args.dark_lowest_color if g_args.dark_lowest_color else (255, 0, 0, 255)        # red
            color_bg = g_args.dark_lowest_bg if g_args.dark_lowest_bg else (0, 0, 0, 0)
        elif bat_perc <= PERCENT_LOW:
            color = g_args.dark_low_color if g_args.dark_low_color else (255, 255, 0, 255)            # yellow
            color_bg = g_args.dark_low_bg if g_args.dark_low_bg else (0, 0, 0, 0)
        else:
            color = g_args.dark_color if g_args.dark_color else (255, 255, 255, 255)                  # white
            color_bg = g_args.dark_bg if g_args.dark_bg else (0, 0, 0, 0)
    
    return tuple(color), tuple(color_bg)


def change_tray_ico(img_main: Image, img: list[Image], bat_perc: int, charging: bool, light_theme: bool) -> Image:
    """ Вставляет на значок Image-объекты с нужными цифрами и батареей в правильные места и нужного цвета. """

    # если нет батареи (мы на PC):
    if bat_perc == NO_BAT:
        return img[20]      # в элементе "20" находится изображение с отсутствующей батареей.

    digit_size_x = DIGIT_SIZE_X
    ifx = INDENT_FIRST_NUMBER_X
    ify = INDENT_NUMBERS_Y
    ibn = INDENT_BETWEEN_NUMBERS
    iby = INDENT_BATTERY_Y
    rm = RM

    color, color_bg = get_color_and_bg(light_theme, charging, bat_perc)

    # если цифры упираются в границе значка и фон не прозрачный - отодвинем чуть ниже, а то не красиво:
    if ify == 0 and color_bg[3] > 0:
        ify = 1

    # очищает значок от предыдущих цифр прозрачным прямоугольником:
    img_main.paste(im=color_bg, box=(0, 0, MAIN_SIZE_X * rm, MAIN_SIZE_Y * rm))

    # располагает цифры на значок в нужные места:
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

        img_main.paste(im=color, box=(ifx * rm, ify * rm), mask=img[n_tens])
        img_main.paste(im=color, box=((ifx + digit_size_x + ibn) * rm, ify * rm), mask=img[n_ones])

    # располагает рисунок батареи на значок:
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

    while True:
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


def parse_console_arguments() -> argparse.Namespace:
    """ Считывает аргументы, переданные в командную строку при запуске программы. """
    
    parser = argparse.ArgumentParser(description='Set some colors, different from default.')

    parser.add_argument('-lcc', '--light_charging_color', dest='light_charging_color', nargs=4, type=int)
    parser.add_argument('-lcb', '--light_charging_bg', dest='light_charging_bg', nargs=4, type=int)
    parser.add_argument('-lltc', '--light_lowest_color', dest='light_lowest_color', nargs=4, type=int)
    parser.add_argument('-lltb', '--light_lowest_bg', dest='light_lowest_bg', nargs=4, type=int)
    parser.add_argument('-llc', '--light_low_color', dest='light_low_color', nargs=4, type=int)
    parser.add_argument('-llb', '--light_low_bg', dest='light_low_bg', nargs=4, type=int)
    parser.add_argument('-lc', '--light_color', dest='light_color', nargs=4, type=int)
    parser.add_argument('-lb', '--light_bg', dest='light_bg', nargs=4, type=int)

    parser.add_argument('-dcc', '--dark_charging_color', dest='dark_charging_color', nargs=4, type=int)
    parser.add_argument('-dcb', '--dark_charging_bg', dest='dark_charging_bg', nargs=4, type=int)
    parser.add_argument('-dltc', '--dark_lowest_color', dest='dark_lowest_color', nargs=4, type=int)
    parser.add_argument('-dltb', '--dark_lowest_bg', dest='dark_lowest_bg', nargs=4, type=int)
    parser.add_argument('-dlc', '--dark_low_color', dest='dark_low_color', nargs=4, type=int)
    parser.add_argument('-dlb', '--dark_low_bg', dest='dark_low_bg', nargs=4, type=int)
    parser.add_argument('-dc', '--dark_color', dest='dark_color', nargs=4, type=int)
    parser.add_argument('-db', '--dark_bg', dest='dark_bg', nargs=4, type=int)

    args = parser.parse_args()

    return args


def main():
    """ Создаёт объект значка в трее с изображением и меню. """

    tray_menu = pystray.Menu(pystray.MenuItem(text='Refresh % !', action=on_refresh_item, default=True),
                             pystray.MenuItem(text='Exit !', action=on_exit_item))
    tray = pystray.Icon(name='Battery Percent', icon=img_tray_ico, title=None, menu=tray_menu)

    tray.SETUP_THREAD_TIMEOUT = 0

    tray.run(setup=auto_check_battery_percent)


if __name__ == '__main__':
    g_prev_bat_percent = None
    g_prev_charging = None
    g_prev_light_theme = None
    g_stop = False
    g_args = parse_console_arguments()

    img_tray_ico = Image.new(mode='RGBA', size=(MAIN_SIZE_X * RM, MAIN_SIZE_Y * RM), color=(0, 0, 0, 0))
    img_digits_list = get_img_digits_list()

    main()

# todo: если есть изображения цифр и батареи в определённой папке - по_CROP_ать их оттуда и заполнить список ими.
# todo: view w.o. bat w. big nums ?
# todo: many screen resolutions...
# todo: 125%+ ?
# todo: Win-API callback ?..
