
Скрипт для тех, кому, как и мне, надоело наводить мышкой на значок батареи, чтобы узнать процент заряда.

Отображает процент заряда батареи в значке в трее (вместе с рисунком батареи).

![image](https://github.com/user-attachments/assets/0953e1d6-b5c3-4f1b-8c73-6494c1baf767)

Должен работать на Windows, Linux, Mac, но тестировался только на Win 10.

Можно задавать разные цвета значка и фона для:
- тёмной и светлой тем
- подключена или нет зарядка
- низкий процент заряда (например, < 20)
- очень низкий процент заряда (например, < 10)

Эти цвета можно задавать с помощью аргументов (см. parse_console_arguments()),

например: 

C:\BatteryPercent\venv_BatteryPercent\Scripts\python.exe C:\BatteryPercent\main.py --light_bg 0 0 255 255 --dark_bg 255 0 0 255 --dark_charging_color 255 255 255 255 --dark_charging_bg 0 255 0 255 --light_charging_color 0 0 0 255 --light_charging_bg 0 255 0 255

в .cmd/.bat-файле.

Или

C:\BatPerc.exe -dcb 0 0 100 255 -db 100 0 0 255

в свойствах ярлыка к exe-файлу:

![image](https://github.com/user-attachments/assets/ae5254b2-1869-4c74-ba4d-1a062de73325)

Если не задавать аргументов - будут цвета по умолчанию.
