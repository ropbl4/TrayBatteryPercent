import psutil
import pystray
from PIL import Image, ImageFont, ImageDraw, ImageColor


def main():
    battery = psutil.sensors_battery()
    print(f'{battery = }')
    battery_percent = battery.percent
    print(f'{battery_percent = }')
    print(psutil.boot_time())
    sensors_temperatures = psutil.sensors_temperatures()
    print(sensors_temperatures)


def os_test():
    img = Image.open('D:/bat2.png')
    print(img.format, img.size, img.mode)

    draw = ImageDraw.Draw(img)
    draw.text(xy=(3, 0), text='87', fill=ImageColor.colormap['white'])

    img.show()


if __name__ == '__main__':
    os_test()
