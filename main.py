import psutil
import pystray
from PIL import Image
from random import randint
from time import sleep

IMAGE_BATTERY_PATH = 'D:/bat.png'
IMAGE_DIGITS_PATH = 'D:/digits.png'
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

    return img_digit


def change_percent_on_image(img_bat_original):
    print("i'm in change_percent_on_image()")
    img_bat_with_nums = img_bat_original.copy()
    # img_original.show()
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
    # img_original.show()
    img_bat_with_nums.show()
    return img_bat_with_nums


def on_click(icon, item):
    icon.icon = change_percent_on_image(img_battery)
    # print("I'm in on_click")


def auto_check_battery_percent(self):
    self.visible = True
    print('===== i was in auto_check_battery_percent =====')
    for _ in range(0):
        self.icon = change_percent_on_image(img_battery)
        sleep(SEC)


def main():
    tray_menu = pystray.Menu(pystray.MenuItem('Random percent !', on_click))
    tray = pystray.Icon(name='Battery Percent', icon=change_percent_on_image(img_battery), menu=tray_menu)

    tray.run(auto_check_battery_percent)


if __name__ == '__main__':
    img_battery = Image.open(IMAGE_BATTERY_PATH)
    print(img_battery.format, img_battery.size, img_battery.mode)
    # img_battery.show()
    img_digits = Image.open(IMAGE_DIGITS_PATH)
    print(img_battery.format, img_battery.size, img_battery.mode)
    # img_digits.show()

    main()
