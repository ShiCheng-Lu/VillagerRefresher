from PIL import Image, ImageGrab

import pyautogui # import this, very important
import pygetwindow
import pydirectinput
import time

import const

def set_game_const():
    windows = pygetwindow.getWindowsWithTitle('Minecraft')
    if (len(windows) == 0):
        return False
    # find the app with 'Minecraft' as it's title
    duplicate = False
    minecraft = None
    for window in windows:
        print(window.title)
        if (window.title == 'Minecraft'):
            minecraft = window
            # if there are two 'Minecraft' windows
            if duplicate:
                return False
            duplicate = True
    if minecraft == None:
        return False

    const.GAME.LEFT   = minecraft.left
    const.GAME.RIGHT  = minecraft.right
    const.GAME.TOP    = minecraft.top
    const.GAME.BOTTOM = minecraft.bottom
    const.GAME.set_attr()

def set_menu_const():
    image = ImageGrab.grab()
    
    app_shadow = 32

    half_x = const.GAME.LEFT + const.GAME.WIDTH // 2
    half_y = const.GAME.TOP + const.GAME.HEIGHT // 2
    # get the left side of menu
    for x in range(const.GAME.LEFT + app_shadow, half_x):
        if image.getpixel((x, half_y)) == const.BLACK:
            const.MENU.LEFT = x
            break
    # get the right side of menu
    for x in range(const.GAME.RIGHT - app_shadow, half_x, -1):
        if image.getpixel((x, half_y)) == const.BLACK:
            const.MENU.RIGHT = x + 1
            break
    # get the top side of menu
    for y in range(const.GAME.TOP + app_shadow, half_y):
        if image.getpixel((half_x, y)) == const.BLACK:
            const.MENU.TOP = y
            break
    # get the bottom side of menu
    for y in range(const.GAME.BOTTOM - app_shadow, half_y, -1):
        if image.getpixel((half_x, y)) == const.BLACK:
            const.MENU.BOTTOM = y + 1
            break
    
    const.MENU.set_attr()
    const.MENU_SIZE = const.MENU.WIDTH // const.MIN_MENU_WIDTH

def set_check_boxes():
    # menu check
    const.MENU_CHECK.TOP = const.MENU.TOP
    const.MENU_CHECK.RIGHT = const.MENU.RIGHT
    const.MENU_CHECK.LEFT = const.MENU.RIGHT - const.MENU_SIZE * 4
    const.MENU_CHECK.BOTTOM = const.MENU.TOP + const.MENU_SIZE * 4
    const.MENU_CHECK.set_attr()
    # mouse loc
    const.MOUSE_2 = (const.MENU.LEFT + const.MENU_SIZE * 100, const.MENU.TOP + const.MENU_SIZE * 50)
    # trade check
    pydirectinput.moveTo(*const.MOUSE_2)
    pydirectinput.move(0, 1)

    image = ImageGrab.grab((const.MOUSE_2[0],
                            const.MOUSE_2[1], 
                            const.MOUSE_2[0] + const.MENU_SIZE * 20, 
                            const.MOUSE_2[1] + const.MENU_SIZE * 10))

    const.TRADE_2.LEFT   = const.MOUSE_2[0]   + get_text_left(image, const.TEXT_GREY)
    const.TRADE_2.RIGHT  = const.TRADE_2.LEFT + const.MENU_SIZE * 120
    const.TRADE_2.TOP    = const.MOUSE_2[1]   + get_text_top(image, const.TEXT_GREY) + 1
    const.TRADE_2.BOTTOM = const.TRADE_2.TOP  + const.MENU_SIZE * 8 + 1
    const.TRADE_2.set_attr()
    # move to topleft of menu
    pydirectinput.moveTo(const.MENU.LEFT, const.MENU.TOP)


def get_text_left(image, colour):
    for x in range(image.width):
        for y in range(image.height):
            if image.getpixel((x, y)) == colour:
                return x

def get_text_top(image, colour):
    for y in range(image.height):
        for x in range(image.width):
            if image.getpixel((x, y)) == colour:
                return y

def setup_all():
    if set_game_const() == False:
        quit()
    if set_menu_const() == False:
        quit()
    if set_check_boxes() == False:
        quit()


if __name__ == "__main__":
    # setup()
    time.sleep(3)

    set_game_const()
    print(const.GAME.BOX)
    set_menu_const()
    set_check_boxes()
    
    ImageGrab.grab(const.TRADE_2.BOX).show()
