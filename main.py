import psutil
import pystray
from PIL import Image
from time import sleep

# IMAGES_PATH = 'D:/img/'
# IMAGE_BATTERY_PATH = IMAGES_PATH + 'bat.ico'
# IMAGE_DIGITS_PATH = IMAGES_PATH + 'digits/digits.ico'

REFRESH_PAUSE_SEC = 5

MAIN_SIZE_X = 16
MAIN_SIZE_Y = 16
DIGIT_SIZE_X = 5
DIGIT_SIZE_Y = 6
BAT_SIZE_X = 16
BAT_SIZE_Y = 7

INDENT_FIRST_NUMBER_X = 3
INDENT_FIRST_NUMBER_Y = 0
INDENT_BETWEEN_NUMBERS = 0
INDENT_BATTERY_Y = 9

ICO_RESOLUTION_MULTIPLIER = 2  # 1 for 16x16, 2 for 32x32, ...


def get_battery_percent() -> int:  # TODO: убедиться, что psutil.sensors_battery().percent - это int
    """ Возвращает текущий процент батареи (целое число). """

    battery = psutil.sensors_battery()  # TODO: добавить статус подключённой зарядки ?
    print(f'{battery = }')
    battery_percent = battery.percent
    print(f'{battery_percent = }')

    # from random import randint
    #
    # # rand_category = 2
    # rand_category = randint(1, 5)
    # if rand_category == 1:
    #     battery_percent = 100
    # elif rand_category == 2:
    #     battery_percent = randint(0, 9)
    # else:
    #     battery_percent = randint(0, 100)  # for tests
    # print(f'Random {battery_percent = }')

    # battery_percent = change_percent_on_image.cur_bp - 1
    # battery_percent = g_current_battery_percent - 1

    return battery_percent


def set_px(img: Image, px: list[int], col: str = 'white') -> None:
    """ Рисует пиксели с учётом их требуемой "ширины" для нужного разрешения. """

    rm = ICO_RESOLUTION_MULTIPLIER

    if len(px) == 2:
        px.extend((px[0], px[1]))

    img.paste(im=col, box=(px[0] * rm, px[1] * rm, (px[2] + 1) * rm, (px[3] + 1) * rm))


def create_img_digits_list() -> list[Image]:
    """ Создаёт (рисует) список изображений с цифрами и батареей. """

    digit_size_x = DIGIT_SIZE_X
    digit_size_y = DIGIT_SIZE_Y
    bat_size_x = BAT_SIZE_X
    bat_size_y = BAT_SIZE_Y

    rm = ICO_RESOLUTION_MULTIPLIER

    img = []

    for _ in range(10):
        img.append(Image.new(mode='RGBA', size=(digit_size_x * rm, digit_size_y * rm), color=(0, 0, 0, 0)))

    for _ in range(10):
        img.append(Image.new(mode='RGBA', size=(bat_size_x * rm, bat_size_y * rm), color=(0, 0, 0, 0)))

    # ===== 0 =====
    set_px(img=img[0], px=[0, 1, 0, 4])
    set_px(img=img[0], px=[3, 1, 3, 4])
    set_px(img=img[0], px=[1, 0, 2, 0])
    set_px(img=img[0], px=[1, 5, 2, 5])
    # -------------

    # ===== 1 =====
    set_px(img=img[1], px=[1, 1])
    set_px(img=img[1], px=[2, 0, 2, 4])
    set_px(img=img[1], px=[1, 5, 3, 5])
    # -------------

    # ===== 2 =====
    set_px(img=img[2], px=[0, 1])
    set_px(img=img[2], px=[1, 0, 2, 0])
    set_px(img=img[2], px=[3, 1, 3, 2])
    set_px(img=img[2], px=[2, 3])
    set_px(img=img[2], px=[1, 4])
    set_px(img=img[2], px=[0, 5, 3, 5])
    # -------------

    # ===== 3 =====
    set_px(img=img[3], px=[0, 1])
    set_px(img=img[3], px=[1, 0, 2, 0])
    set_px(img=img[3], px=[3, 1])
    set_px(img=img[3], px=[2, 2])
    set_px(img=img[3], px=[3, 3, 3, 4])
    set_px(img=img[3], px=[1, 5, 2, 5])
    set_px(img=img[3], px=[0, 4])
    # -------------

    # ===== 4 =====
    set_px(img=img[4], px=[3, 0, 3, 5])
    set_px(img=img[4], px=[2, 1])
    set_px(img=img[4], px=[1, 2])
    set_px(img=img[4], px=[0, 3])
    set_px(img=img[4], px=[0, 4, 4, 4])
    # -------------

    # ===== 5 =====
    set_px(img=img[5], px=[0, 0, 3, 0])
    set_px(img=img[5], px=[0, 1, 0, 2])
    set_px(img=img[5], px=[0, 2, 2, 2])
    set_px(img=img[5], px=[3, 3, 3, 4])
    set_px(img=img[5], px=[0, 5, 2, 5])
    # -------------

    # ===== 6 =====
    set_px(img=img[6], px=[1, 0, 2, 0])
    set_px(img=img[6], px=[1, 2, 2, 2])
    set_px(img=img[6], px=[1, 5, 2, 5])
    set_px(img=img[6], px=[0, 1, 0, 4])
    set_px(img=img[6], px=[3, 3, 3, 4])
    # -------------

    # ===== 7 =====
    set_px(img=img[7], px=[0, 0, 3, 0])
    set_px(img=img[7], px=[3, 1, 3, 2])
    set_px(img=img[7], px=[2, 3])
    set_px(img=img[7], px=[1, 4, 1, 5])
    # -------------

    # ===== 8 =====
    set_px(img=img[8], px=[1, 0, 2, 0])
    set_px(img=img[8], px=[1, 2, 2, 2])
    set_px(img=img[8], px=[1, 5, 2, 5])
    set_px(img=img[8], px=[0, 1])
    set_px(img=img[8], px=[3, 1])
    set_px(img=img[8], px=[0, 3, 0, 4])
    set_px(img=img[8], px=[3, 3, 3, 4])
    # -------------

    # ===== 9 =====
    set_px(img=img[9], px=[1, 0, 2, 0])
    set_px(img=img[9], px=[1, 3, 2, 3])
    set_px(img=img[9], px=[1, 5, 2, 5])
    set_px(img=img[9], px=[0, 1, 0, 2])
    set_px(img=img[9], px=[3, 1, 3, 4])
    # -------------

    # ==== Bat ====
    # ===== 0 =====
    set_px(img=img[10], px=[1, 0, 13, 0])   # верхняя граница
    set_px(img=img[10], px=[1, 6, 13, 6])   # нижняя граница
    set_px(img=img[10], px=[1, 0, 1, 5])    # левая граница
    set_px(img=img[10], px=[13, 0, 13, 5])  # правая граница
    set_px(img=img[10], px=[14, 2, 14, 4])  # нос батареи

    # Заполненность:
    # ===== 10 ====
    img[11] = img[10].copy()
    set_px(img=img[11], px=[3, 2, 3, 4])
    # -------------

    # ===== 20 ====
    img[12] = img[10].copy()
    set_px(img=img[12], px=[3, 2, 4, 4])
    # -------------

    # ===== 30 ====
    img[13] = img[10].copy()
    set_px(img=img[13], px=[3, 2, 5, 4])
    # -------------

    # ===== 40 ====
    img[14] = img[10].copy()
    set_px(img=img[14], px=[3, 2, 6, 4])
    # -------------

    # ===== 50 ====
    img[15] = img[10].copy()
    set_px(img=img[15], px=[3, 2, 7, 4])
    # -------------

    # ===== 60 ====
    img[16] = img[10].copy()
    set_px(img=img[16], px=[3, 2, 8, 4])
    # -------------

    # ===== 70 ====
    img[17] = img[10].copy()
    set_px(img=img[17], px=[3, 2, 9, 4])
    # -------------

    # ===== 80 ====
    img[18] = img[10].copy()
    set_px(img=img[18], px=[3, 2, 10, 4])
    # -------------

    # ===== 90 ====
    img[19] = img[10].copy()
    set_px(img=img[19], px=[3, 2, 11, 4])
    # -------------

    return img


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
        return create_img_digits_list()


def change_percent_on_image(img_main: Image, img: list[Image], bat_perc: int) -> Image:
    """ Вставляет на значок изображения с нужными цифрами и батареей в правильные места. """
    print('I refresh %')
    digit_size_x = DIGIT_SIZE_X
    ifx = INDENT_FIRST_NUMBER_X
    ify = INDENT_FIRST_NUMBER_Y
    ibn = INDENT_BETWEEN_NUMBERS
    iby = INDENT_BATTERY_Y
    rm = ICO_RESOLUTION_MULTIPLIER

    # # получаем % заряда батареи:
    # bat_perc = get_battery_percent()     # TODO: вынести отдельно ?

    # if bat_perc == change_percent_on_image.cur_bp:
    #     print('return')
    #     return
    #
    # print('I was after bet_num == current...')
    #
    # change_percent_on_image.cur_bp = bat_perc

    # очищаем значок от предыдущих цифр прозрачным прямоугольником:
    img_main.paste(im='#00000000', box=(0, 0, MAIN_SIZE_X * rm, DIGIT_SIZE_Y * rm))
    # TODO: перерис. только нужные цифры
    
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
        n1 = bat_perc // 10
        n2 = bat_perc % 10
        n_bat = n1 + 10

        if n1 == 1:
            ifx -= 1

        img_main.paste(im=img[n1], box=(ifx * rm, ify * rm))
        img_main.paste(im=img[n2], box=((ifx + digit_size_x + ibn) * rm, ify * rm))

    # располагаем рисунок батареи на значок:
    img_main.paste(im=img[n_bat], box=(0, iby * rm))

    return img_main


def on_click_item(tray, item):
    """ Обработчик клика/пункта меню для pystray. """

    tray.icon.show()


def on_exit_and_show_item(tray):
    """ Обработчик пункта меня Exit (завершаем программу, убираем значок). """

    tray.icon.show()
    tray.stop()


def on_refresh_item(tray):
    """ Принудительное обновление изображения значка (даже если % совпадает). """

    global g_current_battery_percent

    battery_percent = get_battery_percent()
    g_current_battery_percent = battery_percent

    tray.icon = change_percent_on_image(img_tray_ico, img_digits_list, battery_percent)


def on_exit_item(tray):
    """ Обработчик пункта меню Exit (завершает программу). """

    tray.stop()


def auto_check_battery_percent(tray) -> None:
    """ Авто-проверка процента батареи (в отдельном потоке средствами pystray). """

    global g_current_battery_percent

    tray.visible = True
    print('===== i was in auto_check_battery_percent =====')
    for _ in range(1000000000):
        battery_percent = get_battery_percent()

        if battery_percent != g_current_battery_percent:
            g_current_battery_percent = battery_percent
            tray.icon = change_percent_on_image(img_tray_ico, img_digits_list, battery_percent)

        sleep(REFRESH_PAUSE_SEC)
        print(f'{_ = }')


def main():
    """ Создаёт объект значка в трее с изображением и меню. """

    global g_current_battery_percent
    # change_percent_on_image.cur_bp = 101

    battery_percent = get_battery_percent()
    g_current_battery_percent = battery_percent

    tray_ico = change_percent_on_image(img_tray_ico, img_digits_list, battery_percent)

    tray_menu = pystray.Menu(pystray.MenuItem(text='Refresh % !', action=on_refresh_item, default=True),
                             pystray.MenuItem(text='Exit !', action=on_exit_item))

    tray = pystray.Icon(name='Battery Percent', icon=tray_ico, menu=tray_menu)

    tray.run(auto_check_battery_percent)
    # tray.run()


if __name__ == '__main__':
    g_current_battery_percent = 101
    img_tray_ico = Image.new(mode='RGBA',
                             size=(MAIN_SIZE_X * ICO_RESOLUTION_MULTIPLIER, MAIN_SIZE_Y * ICO_RESOLUTION_MULTIPLIER),
                             color=(0, 0, 0, 0))
    img_digits_list = get_img_digits_list()

    main()
