import psutil
import pystray
from infi.systray import SysTrayIcon
from PIL import Image
from random import randint
from time import sleep


IMAGES_PATH = 'D:/img/'
IMAGE_BATTERY_PATH = IMAGES_PATH + 'bat.ico'
IMAGE_DIGITS_PATH = IMAGES_PATH + 'digits.ico'
INDENT_DIGITS_FROM_HEIGHT = 0
SEC = 5


def get_battery_percent():
    # battery = psutil.sensors_battery()
    # print(f'{battery = }')
    # battery_percent = battery.percent
    # print(f'{battery_percent = }')

    battery_percent = randint(0, 100)    # for tests
    print(f'Random {battery_percent = }')

    return battery_percent


def get_digit_img(int_digit):
    start_pixel_w = 0                   # from 0, include
    start_pixel_h = int_digit * 6
    end_pixel_w = 6                     # from 0, exclude
    end_pixel_h = start_pixel_h + 6

    img_digit = img_digits.crop((start_pixel_w, start_pixel_h, end_pixel_w, end_pixel_h))
    img_digit = img_digit.convert(mode='1', colors=1)

    return img_digit


def change_percent_on_image2(img_bat_original):
    print("i'm in change_percent_on_image()")
    img_bat_with_nums = img_bat_original.copy()
    # img_bat_with_nums = img_bat_with_nums.convert(mode='1', colors=1)
    # img_original.show()
    # img_bat_with_nums.show()
    battery_percent = get_battery_percent()

    if battery_percent == 100:
        img_digit_one = get_digit_img(1)
        img_digit_zero = get_digit_img(0)

        img_bat_with_nums.paste(img_digit_one, (0, INDENT_DIGITS_FROM_HEIGHT))
        img_bat_with_nums.paste(img_digit_zero, (4, INDENT_DIGITS_FROM_HEIGHT))
        img_bat_with_nums.paste(img_digit_zero, (10, INDENT_DIGITS_FROM_HEIGHT))
    else:
        if int_digit_tens := battery_percent // 10:
            img_digit_tens = get_digit_img(int_digit_tens)
            print(img_digit_tens.format, img_digit_tens.size, img_digit_tens.mode)
            # img_digit_tens.show()
        int_digit_ones = battery_percent % 10
        img_digit_ones = get_digit_img(int_digit_ones)
        print(img_digit_ones.format, img_digit_ones.size, img_digit_ones.mode)
        # img_digit_ones.show()

        if int_digit_tens > 0:
            # img_bat_with_nums.paste(img_digit_tens, (6, 1, 12, 7))
            img_bat_with_nums.paste(img_digit_tens, (1, INDENT_DIGITS_FROM_HEIGHT))
            img_bat_with_nums.paste(img_digit_ones, (7, INDENT_DIGITS_FROM_HEIGHT))
        else:
            img_bat_with_nums.paste(img_digit_ones, (5, INDENT_DIGITS_FROM_HEIGHT))

    print(img_bat_with_nums.format, img_bat_with_nums.size, img_bat_with_nums.mode)
    # img_bat_with_nums = img_bat_with_nums.convert(mode='L')
    print(img_bat_with_nums.format, img_bat_with_nums.size, img_bat_with_nums.mode)

    # img_original.show()
    # img_bat_with_nums.show()
    # return img_bat_with_nums
    img_bat_with_nums.save(fp=IMAGES_PATH+'tmp.ico', format='ICO', bitmap_format='bmp')

    return IMAGES_PATH+'tmp.ico'


def change_percent_on_image(fake_parameter=None):
    img = Image.new(mode='1', size=(16, 16), color=0)
    color = 255

    offset = 1
    # ============ 1
    img.putpixel(xy=(offset+0, 1), value=color)
    img.putpixel(xy=(offset+1, 0), value=color)
    img.putpixel(xy=(offset+1, 1), value=color)
    img.putpixel(xy=(offset+1, 2), value=color)
    img.putpixel(xy=(offset+1, 3), value=color)
    img.putpixel(xy=(offset+1, 4), value=color)
    img.putpixel(xy=(offset+1, 5), value=color)
    img.putpixel(xy=(offset+0, 5), value=color)
    img.putpixel(xy=(offset+2, 5), value=color)

    offset = 6
    # ============ 2
    img.putpixel(xy=(offset + 0, 1), value=color)
    img.putpixel(xy=(offset + 1, 0), value=color)
    img.putpixel(xy=(offset + 2, 0), value=color)
    img.putpixel(xy=(offset + 3, 1), value=color)
    img.putpixel(xy=(offset + 3, 2), value=color)
    img.putpixel(xy=(offset + 2, 3), value=color)
    img.putpixel(xy=(offset + 1, 4), value=color)
    img.putpixel(xy=(offset + 0, 5), value=color)
    img.putpixel(xy=(offset + 1, 5), value=color)
    img.putpixel(xy=(offset + 2, 5), value=color)
    img.putpixel(xy=(offset + 3, 5), value=color)

    # img.show()

    # return img
    img.save(fp=IMAGES_PATH + 'tmp.ico', format='ICO', bitmap_format='bmp')

    return IMAGES_PATH + 'tmp.ico'


def on_click(icon, item):
    icon.icon = change_percent_on_image(img_battery)
    icon.icon.show()
    # print("I'm in on_click")


def auto_check_battery_percent(self=None):
    # self.visible = True
    print('===== i was in auto_check_battery_percent =====')
    for _ in range(10):
        self.icon = change_percent_on_image(img_battery)
        sleep(SEC)
        print(f'{_ = }')


def say_hello(systray):
    print("Hello")


def test():
    menu_options = (("Say Hello", None, say_hello),)
    # systray = SysTrayIcon(IMAGES_PATH + "bat_saved.ico", "", menu_options)
    systray = SysTrayIcon(change_percent_on_image(), "", menu_options)
    systray.start()
    # auto_check_battery_percent()


def main():
    tray_menu = pystray.Menu(pystray.MenuItem('Random percent !', on_click))
    # tray = pystray.Icon(name='Battery Percent', icon=Image.open(IMAGES_PATH+'тест.ico'), menu=tray_menu)
    tray = pystray.Icon(name='Battery Percent', icon=Image.open(IMAGES_PATH + 'tmp.ico'), menu=tray_menu)
    # tray = pystray.Icon(name='Battery Percent', icon=change_percent_on_image(img_battery), menu=tray_menu)

    # tray.run(auto_check_battery_percent)
    tray.run()


if __name__ == '__main__':
    # img_battery = Image.open(IMAGE_BATTERY_PATH)
    # img_battery.save(fp=IMAGES_PATH + 'bat_saved.ico', format='ICO', bitmap_format='bmp')

    # print(img_battery.format, img_battery.size, img_battery.mode)
    # img_battery.show()
    # img_digits = Image.open(IMAGE_DIGITS_PATH)
    # print(img_digits.format, img_digits.size, img_digits.mode)
    # img_digits.show()

    # main()
    test()
