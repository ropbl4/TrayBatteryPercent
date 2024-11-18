from PIL import Image

MAIN_SIZE_X = 16
MAIN_SIZE_Y = 16
DIGIT_SIZE_X = 5
DIGIT_SIZE_Y = 6
BAT_SIZE_X = 16
BAT_SIZE_Y = 7

ICO_RESOLUTION_MULTIPLIER = 2  # 1 for 16x16, 2 for 32x32, ...


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
    no_bat_size_x = MAIN_SIZE_X
    no_bat_size_y = MAIN_SIZE_Y

    rm = ICO_RESOLUTION_MULTIPLIER

    img = []

    # img[0-9]:
    for _ in range(10):
        img.append(Image.new(mode='RGBA', size=(digit_size_x * rm, digit_size_y * rm), color=(0, 0, 0, 0)))

    # img[10-19]:
    for _ in range(10):
        img.append(Image.new(mode='RGBA', size=(bat_size_x * rm, bat_size_y * rm), color=(0, 0, 0, 0)))

    # img[20]:
    img.append(Image.new(mode='RGBA', size=(no_bat_size_x * rm, no_bat_size_y * rm), color=(0, 0, 0, 0)))

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

    # === No Bat ==
    img[20].paste(im=img[11], box=(0, 5 * rm))
    for i in range(no_bat_size_x):
        set_px(img=img[20], px=[i, i], col='red')
    for i in range(no_bat_size_x):
        set_px(img=img[20], px=[no_bat_size_x - 1 - i, i], col='red')
    # -------------

    return img
