import psutil
import pystray
from infi.systray import SysTrayIcon
from PIL import Image
from random import randint
from time import sleep

IMAGES_PATH = 'D:/img/'
IMAGE_BATTERY_PATH = IMAGES_PATH + 'bat.ico'
IMAGE_DIGITS_PATH = IMAGES_PATH + 'digits/digits.ico'
INDENT_DIGITS_FROM_HEIGHT = 0
SEC = 5


def get_battery_percent() -> int:   # TODO: убедиться, что psutil.sensors_battery().percent - это int
    """ Возвращает текущий процент батареи (целое число). """

    # battery = psutil.sensors_battery()
    # print(f'{battery = }')
    # battery_percent = battery.percent
    # print(f'{battery_percent = }')

    battery_percent = randint(0, 100)    # for tests
    print(f'Random {battery_percent = }')

    return battery_percent


def get_digit_img(int_digit):   # TODO: возвращает объект изображения (объект Pillow или ...)
    """ Находит часть изображения с нужной цифрой и возвращает его, как объект изображения. """

    start_pixel_w = 0                   # from 0, include
    start_pixel_h = int_digit * 6
    end_pixel_w = 6                     # from 0, exclude
    end_pixel_h = start_pixel_h + 6

    # TODO: img_digits сейчас глобальная; надо или передать, или, может, она нужна только тут - тогда здесь и получить.
    # img_digits = Image.open('D:\\- Volume2-master\\Skins\\Volume2 Default Light\\Digits.png')
    img_digits = Image.open(IMAGES_PATH+'Volume2 Default Light/Digits.png')
    img_digit = img_digits.crop((start_pixel_w, start_pixel_h, end_pixel_w, end_pixel_h))
    # img_digit = img_digit.convert(mode='1', colors=1)     # надо ли это ?..

    return img_digit


def change_percent_on_image2(img_bat_original):
    """ Помещает цифры на значок батареи (в правильные места в нужном количестве). """

    print("i'm in change_percent_on_image()")
    img_bat_with_nums = img_bat_original.copy()
    # img_bat_with_nums = img_bat_with_nums.convert(mode='1', colors=1)
    # img_original.show()
    # img_bat_with_nums.show()
    # battery_percent = get_battery_percent()
    battery_percent = 26

    if battery_percent == 100:
        img_digit_one = get_digit_img(1)
        img_digit_zero = get_digit_img(0)

        img_bat_with_nums.paste(img_digit_one, (0, INDENT_DIGITS_FROM_HEIGHT))
        img_bat_with_nums.paste(img_digit_zero, (4, INDENT_DIGITS_FROM_HEIGHT))
        img_bat_with_nums.paste(img_digit_zero, (10, INDENT_DIGITS_FROM_HEIGHT))
    else:
        if int_digit_tens := battery_percent // 10:
            img_digit_tens = get_digit_img(int_digit_tens)
            print(img_digit_tens.format, img_digit_tens.size, img_digit_tens.mode, '   -   img_digit_tens (cutted digit for tens)')
            # img_digit_tens.show()
        int_digit_ones = battery_percent % 10
        img_digit_ones = get_digit_img(int_digit_ones)
        print(img_digit_ones.format, img_digit_ones.size, img_digit_ones.mode, '   -   img_digit_ones (cutted digit for ones)')
        # img_digit_ones.show()

        if int_digit_tens > 0:
            # img_bat_with_nums.paste(img_digit_tens, (6, 1, 12, 7))
            img_bat_with_nums.paste(img_digit_tens, (1, INDENT_DIGITS_FROM_HEIGHT))
            img_bat_with_nums.paste(img_digit_ones, (7, INDENT_DIGITS_FROM_HEIGHT))
        else:
            img_bat_with_nums.paste(img_digit_ones, (5, INDENT_DIGITS_FROM_HEIGHT))

    print(img_bat_with_nums.format, img_bat_with_nums.size, img_bat_with_nums.mode, '   -   img_bat_with_nums (result image)')
    # img_bat_with_nums = img_bat_with_nums.convert(mode='L')
    # print(img_bat_with_nums.format, img_bat_with_nums.size, img_bat_with_nums.mode)

    # img_original.show()
    # img_bat_with_nums.show()
    return img_bat_with_nums
    # img_bat_with_nums.save(fp=IMAGES_PATH+'tmp.ico', format='ICO', bitmap_format='bmp')

    # return IMAGES_PATH+'tmp.ico'


# def bake_several_pngs_to_ico(sourcefiles, targetfile):
#     """ Объединяет несколько png в один ico (скопировал откуда-то).
#         Использовал для одного изображения в качестве очередного варианта конвертации. """
#
#     from pathlib import Path
#
#     # Write the global header
#     number_of_sources = len(sourcefiles)
#     data = bytes((0, 0, 1, 0, number_of_sources, 0))
#     offset = 6 + number_of_sources * 16
#
#     # Write the header entries for each individual image
#     for sourcefile in sourcefiles:
#         img = Image.open(sourcefile)
#         data += bytes((img.width, img.height, 0, 0, 1, 0, 32, 0, ))
#         bytesize = Path(sourcefile).stat().st_size
#         data += bytesize.to_bytes(4, byteorder="little")
#         data += offset.to_bytes(4, byteorder="little")
#         offset += bytesize
#
#     # Write the individual image data
#     for sourcefile in sourcefiles:
#         data += Path(sourcefile).read_bytes()
#
#     # Save the icon file
#     Path(targetfile).write_bytes(data)


def set_px(img: Image, px: list[int], col: str = 'white'):
    """ Рисуем пиксели с учётом их требуемой "ширины" для нужного разрешения. """

    rm = 2      # ico Resolution Multiplier (1 for 16x16, 2 for 32x32, ...)

    if len(px) == 2:
        px.extend((px[0], px[1]))

    img.paste(im=col, box=(px[0] * rm, px[1] * rm, (px[2]+1) * rm, (px[3]+1) * rm))


def create_img_digits_list() -> list[Image]:
    """ Создаём (рисуем) список изображений с цифрами """

    main_size_x = 16    # размер значка в трее - X
    main_size_y = 16    # размер значка в трее - Y
    digit_size_x = 5    # размер цифры - X
    digit_size_y = 6    # размер цифры - Y
    bat_size_x = 16     # размер батареи - X
    bat_size_y = 7      # размер батареи - Y

    ifx = 2             # Indent First number - X
    ify = 0             # Indent First number - Y
    ibn = 0             # Indent Between Number
    iby = 9             # Indent Battery - Y
    rm = 2              # ico Resolution Multiplier (1 for 16x16, 2 for 32x32, ...)

    img = [None, None, None, None, None, None, None, None, None, None, None]
    # print(img)
    for i in range(9+1):
        img[i] = Image.new(mode='RGBA', size=(digit_size_x * rm, digit_size_y * rm), color=(0, 0, 0, 0))
    # img[4] = Image.new(mode='RGBA', size=(digit_size_x * rm, digit_size_y * rm), color=(0, 0, 0, 0))
    img[10] = Image.new(mode='RGBA', size=(bat_size_x * rm, bat_size_y * rm), color=(0, 0, 0, 0))
    # for i in range(5): print(f'img[{i}] = {img[i]}')
    # quit()
    # img.show()

    # ===== 0 =====
    set_px(img=img[0], px=[0, 1, 0, 4])
    set_px(img=img[0], px=[3, 1, 3, 4])
    set_px(img=img[0], px=[1, 0, 2, 0])
    set_px(img=img[0], px=[1, 5, 2, 5])
    # img[0].show()
    # -------------

    # ===== 1 =====
    set_px(img=img[1], px=[1, 1])
    set_px(img=img[1], px=[2, 0, 2, 4])
    set_px(img=img[1], px=[1, 5, 3, 5])
    # img[1].show()
    # -------------

    # ===== 2 =====
    set_px(img=img[2], px=[0, 1])
    set_px(img=img[2], px=[1, 0, 2, 0])
    set_px(img=img[2], px=[3, 1, 3, 2])
    set_px(img=img[2], px=[2, 3])
    set_px(img=img[2], px=[1, 4])
    set_px(img=img[2], px=[0, 5, 3, 5])
    # img[2].show()
    # -------------

    # ===== 3 =====
    set_px(img=img[3], px=[0, 1])
    set_px(img=img[3], px=[1, 0, 2, 0])
    set_px(img=img[3], px=[3, 1])
    set_px(img=img[3], px=[2, 2])
    set_px(img=img[3], px=[3, 3, 3, 4])
    set_px(img=img[3], px=[1, 5, 2, 5])
    set_px(img=img[3], px=[0, 4])
    # img[3].show()
    # -------------

    # ===== 4 =====
    set_px(img=img[4], px=[3, 0, 3, 5])
    set_px(img=img[4], px=[2, 1])
    set_px(img=img[4], px=[1, 2])
    set_px(img=img[4], px=[0, 3])
    set_px(img=img[4], px=[0, 4, 5, 4])
    # img[4].show()
    # -------------

    # ===== 5 =====
    set_px(img=img[5], px=[0, 0, 3, 0])
    set_px(img=img[5], px=[0, 1, 0, 2])
    set_px(img=img[5], px=[0, 2, 2, 2])
    set_px(img=img[5], px=[3, 3, 3, 4])
    set_px(img=img[5], px=[0, 5, 2, 5])
    # img[5].show()
    # -------------

    # ===== 6 =====
    set_px(img=img[6], px=[1, 0, 2, 0])
    set_px(img=img[6], px=[1, 2, 2, 2])
    set_px(img=img[6], px=[1, 5, 2, 5])
    set_px(img=img[6], px=[0, 1, 0, 4])
    set_px(img=img[6], px=[3, 3, 3, 4])
    img[6].show()
    # -------------

    # ===== 7 =====
    set_px(img=img[7], px=[3, 0, 3, 5])
    img[7].show()
    # -------------

    # ===== 8 =====
    set_px(img=img[8], px=[3, 0, 3, 5])
    img[8].show()
    # -------------

    # ===== 9 =====
    set_px(img=img[9], px=[3, 0, 3, 5])
    img[9].show()
    # -------------

    # ==== Bat ====
    set_px(img=img[10], px=[1, 0, 13, 0])  # верхняя граница
    set_px(img=img[10], px=[1, 6, 13, 6])  # нижняя граница
    set_px(img=img[10], px=[1, 0, 1, 7])  # левая граница
    set_px(img=img[10], px=[13, 0, 13, 7])  # правая граница
    set_px(img=img[10], px=[14, 2, 14, 4])  # нос батареи

    set_px(img=img[10], px=[3, 2, 7, 4])  # заполненность
    # img[10].show()
    # -------------

    return img


def get_from_image_img_digits_list() -> list[Image]:
    """ Вырезаем цифры и батарею с изображений на диске,
        заполняем ими массив объектов PIL.Image. """

    pass


def get_img_digits_list() -> list[Image]:
    """ Возвращает список изображений с цифрами и батареей,
        полученный с картинок или, если их нет, нарисованный. """

    if False:   # если найдена папка /img/ и в ней есть картинка с цифрами и батареей...
        return get_from_image_img_digits_list()
    else:
        return create_img_digits_list()


def change_percent_on_image(img: list[Image]) -> Image:
    """ Так, а какой у нас план ?
        - узнаём % бат.
        - рисуем соотв-е цифры и зн. бат.
        - размещаем на нужные места изобр-я
        - обновляем изобр-е на значке """

    main_size_x = 16    # размер значка в трее - X
    main_size_y = 16    # размер значка в трее - Y
    digit_size_x = 5    # размер цифры - X
    digit_size_y = 6    # размер цифры - Y
    bat_size_x = 16     # размер батареи - X
    bat_size_y = 7      # размер батареи - Y

    ifx = 3             # Indent First number - X
    ify = 0             # Indent First number - Y
    ibn = 0             # Indent Between Number
    iby = 9             # Indent Battery - Y
    rm = 2              # ico Resolution Multiplier (1 for 16x16, 2 for 32x32, ...)

    # img = [None, None, None, None, None, None, None, None, None, None, None]
    # # print(img)
    # img[1] = Image.new(mode='RGBA', size=(digit_size_x * rm, digit_size_y * rm), color=(0, 0, 0, 0))
    # img[4] = Image.new(mode='RGBA', size=(digit_size_x * rm, digit_size_y * rm), color=(0, 0, 0, 0))
    # img[10] = Image.new(mode='RGBA', size=(bat_size_x * rm, bat_size_y * rm), color=(0, 0, 0, 0))
    # # for i in range(5): print(f'img[{i}] = {img[i]}')
    # # quit()
    # # img.show()
    #
    # # ===== 1 =====
    # set_px(img=img[1], px=[1, 1])
    # set_px(img=img[1], px=[2, 0, 2, 4])
    # set_px(img=img[1], px=[1, 5, 3, 5])
    # # -------------
    #
    # # ===== 4 =====
    # set_px(img=img[4], px=[3, 0, 3, 5])
    # set_px(img=img[4], px=[2, 1])
    # set_px(img=img[4], px=[1, 2])
    # set_px(img=img[4], px=[0, 3])
    # set_px(img=img[4], px=[0, 4, 5, 4])
    # # -------------
    #
    # # ==== Bat ====
    # set_px(img=img[10], px=[1, 0, 13, 0])   # верхняя граница
    # set_px(img=img[10], px=[1, 6, 13, 6])   # нижняя граница
    # set_px(img=img[10], px=[1, 0, 1, 7])    # левая граница
    # set_px(img=img[10], px=[13, 0, 13, 7])  # правая граница
    # set_px(img=img[10], px=[14, 2, 14, 4])  # нос батареи
    #
    # set_px(img=img[10], px=[3, 2, 7, 4])    # заполненность
    # # -------------

    # img[1].show()
    # img[4].show()
    # img[10].show()

    img_main = Image.new(mode='RGBA', size=(main_size_x * rm, main_size_y * rm), color=(0, 0, 0, 0))

    import random
    rng1 = random.randint(0, 4)
    rng2 = random.randint(0, 4)

    img_main.paste(im=img[rng1], box=(ifx * rm, ify * rm))
    img_main.paste(im=img[rng2], box=((ifx + digit_size_x + ibn) * rm, ify * rm))
    img_main.paste(im=img[10], box=(0, iby * rm))

    return img_main


# def change_percent_on_image(fake_parameter=None):
#     """ Тесты всякие... В частности, с imageio.v3
#         pystray хочет в качестве изображение именно PIL.Image.Image-объект.
#         infi.systray принимает строку с адресом изображения и ему норм. """
#
#     # img = Image.new(mode='RGB', size=(16, 16), color=0)
#     # img = Image.open(fp=IMAGES_PATH+'bat-58.png')
#     import imageio.v3 as iio
#     import io
#     # img = iio.imread(IMAGES_PATH+'bat-58.png', plugin='ITK')
#
#     '''color = 255, 255, 255, 255
#
#     offset = 1
#     # ============ 1
#     img.putpixel(xy=(offset+0, 1), value=color)
#     img.putpixel(xy=(offset+1, 0), value=color)
#     img.putpixel(xy=(offset+1, 1), value=color)
#     img.putpixel(xy=(offset+1, 2), value=color)
#     img.putpixel(xy=(offset+1, 3), value=color)
#     img.putpixel(xy=(offset+1, 4), value=color)
#     img.putpixel(xy=(offset+1, 5), value=color)
#     img.putpixel(xy=(offset+0, 5), value=color)
#     img.putpixel(xy=(offset+2, 5), value=color)
#
#     offset = 6
#     # ============ 2
#     img.putpixel(xy=(offset + 0, 1), value=color)
#     img.putpixel(xy=(offset + 1, 0), value=color)
#     img.putpixel(xy=(offset + 2, 0), value=color)
#     img.putpixel(xy=(offset + 3, 1), value=color)
#     img.putpixel(xy=(offset + 3, 2), value=color)
#     img.putpixel(xy=(offset + 2, 3), value=color)
#     img.putpixel(xy=(offset + 1, 4), value=color)
#     img.putpixel(xy=(offset + 0, 5), value=color)
#     img.putpixel(xy=(offset + 1, 5), value=color)
#     img.putpixel(xy=(offset + 2, 5), value=color)
#     img.putpixel(xy=(offset + 3, 5), value=color)
#
#     # img.show()
#
#     # return img'''
#
#     img = iio.imread(IMAGES_PATH+'bat-58.ico', mode="RGBA")
#
#     output = io.BytesIO()
#     iio.imwrite(output, img, plugin="pillow", extension=".ico")
#
#     # ICO_NAME = 'tmp8.ico'
#     # iio.imwrite(IMAGES_PATH+ICO_NAME, output)
#     # img.save(fp=IMAGES_PATH+'tmp3.ico', format='ICO', bitmap_format='bmp')
#     # bake_several_pngs_to_ico([IMAGES_PATH+'bat-tr.png'], IMAGES_PATH+'tmp.ico')
#
#     return IMAGES_PATH+'bat-58.ico'


def on_click_item(tray, item):
    """ Обработчик клика/пункта меню для pystray. """

    # icon.icon = change_percent_on_image(img_battery)
    tray.icon.show()


def on_exit_and_show_item(tray):
    """ Обработчик пункта меня Exit (завершаем программу, убираем значок). """

    tray.icon.show()
    tray.stop()


def on_rng_item(tray):
    """ Рандомим % (тестируем отображение цифр) """

    tray.icon = change_percent_on_image(img_digits_list)


def on_exit_item(tray):
    """ Обработчик пункта меня Exit (завершаем программу). """

    tray.stop()


def auto_check_battery_percent(self=None):
    """ Авто-проверка процента батареи (в отдельном потоке средствами pystray).
        Так же пробовал использовать в infi.systray. """

    # self.visible = True
    print('===== i was in auto_check_battery_percent =====')
    for _ in range(10):
        self.icon = change_percent_on_image(img_digits_list)
        sleep(SEC)
        print(f'{_ = }')


def say_hello(systray):
    """ Обработчик клика/пункта меню для infi.systray. """

    print("Hello")


def test():
    """ Тут пробуем infi.systray. """

    menu_options = (("Say Hello", None, say_hello),)
    systray = SysTrayIcon(IMAGES_PATH+get_ico_name(), "", menu_options)
    # systray = SysTrayIcon(IMAGES_PATH+"tmp4__24_32_BPP.ico", "", menu_options)
    # systray = SysTrayIcon(change_percent_on_image(), "", menu_options)

    systray.start()
    # auto_check_battery_percent()


def get_ico_name() -> str:
    """ Возвращаем название изображения, которое сейчас тестируем.
        Сюда же пишем комменты о результате. """

    # ico_name = 'tmp.ico'        # pystray: чёрный фон. Портится в трее сразу же: без обработки (открывается норм).
    # ico_name = 'bat_26.png'     # pystray: прозрачность есть и остаётся, но картинка портится.
    # ico_name = 'bat_26.ico'     # pystray: прозрачность есть и остаётся, картинка портится (чуть лучше, чем png).
    # ico_name = 'bat_26_15x15.png'     # pystray: ошибка при выполнении (как и ..14х14).
    # ico_name = 'bat_26_17x17.png'     # pystray: сжалось ещё сильнее, аж верхний ряд пикс-й на бат. исчез. Пр. сохр.
    # ico_name = 'bat_26_i_15x15.ico'   # pystray: сжалось по-своему (г). Прозр. сохр.
    # ico_name = 'bat_26_i_17x17.ico'   # pystray: сжалось по-своему. Прозр. сохр.

    # ico_name = 'bat 58__8_24_32_BPP.ico'    # pystray: сжалось сильно. Прозр. сохр.
    #                                             # infi: УСПЕХ ! Вообще не сжалось + прозрачность !
    # ico_name = 'bat 58__8_BPP.png'          # pystray: сжалось сильно. Прозр. сохр.
    #                                             # infi: png не работает.
    # ico_name = 'bat__4_BPP.png'             # pystray: сжалось немного, фон чёрный, как и был.
    #                                             # infi: png не работает.
    # ico_name = 'bat__24_32_BPP.ico'         # pystray: сжалось сильнее. Прозр. сохр.
    #                                             # infi: и это УСПЕХ ! (Тут чисто батарея). Белая + прозр. сохр.
    # ico_name = 'bat_saved__32_BPP.ico'      # pystray: сжалось сильнее. Прозр. сохр.
    #                                             # infi: сжалось. Прозр. сохр.
    # ico_name = 'bat_tr__24_32_BPP.png'      # pystray: сжалось сильнее. Прозр. сохр.
    #                                             # infi: png не работает.

    # ico_name = 'test2__dig_black_32_BPP.ico'  # pystray: сжалось немного, прозр., кроме цифр.
    #                                               # infi: сжалось немного, прозр., кроме цифр.
    # ico_name = 'tmp1__24_32_BPP.ico'          # pystray: сжалось, прозр. сохр.
    #                                               # infi: сжалось, прозр. сохр.
    # ico_name = 'tmp2__1_BPP.ico'              # pystray: чуть-чуть сжалось, но потеряла прозрачность.
    #                                               # infi: сжалось сильно, прозр. сохр.
    # ico_name = 'tmp3__8_24_32_BPP.ico'        # pystray: сжалось немного, но фон чёрный.
    #                                               # infi: сжалось очень сильно, прозр. сохр.
    # ico_name = 'tmp4__24_32_BPP.ico'          # pystray: очень сжалось. Прозр. сохр.
    #                                               # infi: и tmp5,6: очень сжалось. Прозр. сохр.
    # ico_name = 'tmp5__24_32_BPP.ico'          # pystray: очень сжалось, фон прозр.
    #                                               # infi: очень сжалось, стала ещё темнее; фон прозр.
    # ico_name = 'tmp6__black_24_BPP.ico'       # pystray: немного сжалось, фон чёрный, как и был.
    #                                               # infi: немного сжалось, чёрный фон был и остался.
    # ico_name = 'тест__4_24_32_BPP.ico'        # pystray: немного сжалось, фон чёрный, как и был.
    #                                               # infi: идеально, но она чёрная
    # ico_name = 'тест__4_BPP.png'              # pystray: немного сжалось, фон чёрный, как и был.
    #                                               # infi: png не работает.
    # ico_name = 'тест_black-из-ico-в-png__24_32_BPP.png'     # pystray: немного сжалось, фон чёрный, как и был.
    #                                                             # infi: png не работает.

    # IMAGES_PATH = 'D:\\- Volume2-master\\Assets\\MainIcon-PNGs\\'
    # ico_name = '16.png'
    # IMAGES_PATH = 'D:\\- Volume2-master\\Skins\\Volume2 Default Light\\'
    # ico_name = 'Volume2 Default Light/Back.png'   # pystray: немного сжалось, прозр. сохр.
    #                                                   # infi: png вообще не может (показывает стандартную виндовую)
    # ico_name = '58 64x64 8 bpp.ico'               # pystray: УСПЕХ ! Впервые на pystray без сжатия + прозр. !
    #                                                 (белый: 238-254 вместо 255, но это не заметно)
    #                                                   # infi: УСПЕХ ! И без сжатия, и белый 255, и прозр.
    # ico_name = '58 64x64 32 BPP.ico'              # Всё ровно так же, как с 8 BPP.
    # ico_name = '58 32x32 8 BPP games_of_transp.ico'   # pystray: УСПЕХ ! Теперь белый 255 и у pystray ! + прозр.
    #                                                       # infi: Тоже всё отлично: белый 255, прозр.
    # ico_name = '58 32x32 32 BPP games_of_transp.ico'  # обе чуть темнее
    # ico_name = '58 32x32 32 BPP del_transp.ico'   # обе отлично: 255 + прозр.
    ico_name = '58 32x32 8 BPP del_transp.ico'    # обе отлично

    return ico_name
    
    
def main():
    """ Тут пробуем pystray. """

    # tray_ico = Image.open(IMAGES_PATH+get_ico_name())
    # tray_ico = change_percent_on_image2(tray_ico)
    tray_ico = change_percent_on_image(img_digits_list)
    # tray_ico.show()

    tray_menu = pystray.Menu(pystray.MenuItem('On click !', on_click_item),
                             pystray.MenuItem('Exit + Show !', on_exit_and_show_item),
                             pystray.MenuItem(text='Randomize % !', action=on_rng_item, default=True),
                             pystray.MenuItem('Exit !', on_exit_item))

    tray = pystray.Icon(name='Battery Percent', icon=tray_ico, menu=tray_menu)
    # tray = pystray.Icon(name='Battery Percent', icon=change_percent_on_image(img_battery), menu=tray_menu)

    # tray.run(auto_check_battery_percent)
    tray.run()


# def test_from_documentation():
#     from PIL import Image, ImageDraw
#
#     def create_image(width, height, color1, color2):
#         # Generate an image and draw a pattern
#         image = Image.new('RGB', (width, height), color1)
#         dc = ImageDraw.Draw(image)
#         dc.rectangle(
#             (width // 2, 0, width, height // 2),
#             fill=color2)
#         dc.rectangle(
#             (0, height // 2, width // 2, height),
#             fill=color2)
#
#         return image
#
#     # In order for the icon to be displayed, you must provide an icon
#     icon = pystray.Icon(
#         'test name',
#         icon=create_image(64, 64, 'black', 'white'))
#
#     # To finally show you icon, call run
#     icon.run()


if __name__ == '__main__':
    # img_battery = Image.open(IMAGE_BATTERY_PATH)
    # img_battery.save(fp=IMAGES_PATH + 'bat_saved.ico', format='ICO', bitmap_format='bmp')

    # print(img_battery.format, img_battery.size, img_battery.mode)
    # img_battery.show()

    # img_digits = Image.open(IMAGE_DIGITS_PATH)

    # print(img_digits.format, img_digits.size, img_digits.mode)
    # img_digits.show()

    # test()
    img_digits_list = get_img_digits_list()

    main()
    # test_from_documentation()
    # change_percent_on_image()
