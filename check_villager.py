from PIL import Image, ImageGrab
import pydirectinput
import time
import const

GREY = (170, 170, 170)
WHITE = (255, 255, 255)

# print out the data
def print_data(data):
    out = ""
    for y in range(len(data[0])):
        for x in range(len(data)):
            if data[x][y]:
                out += "X"
            else:
                out += " "
        out += '\n'
    print(out)

# extract the text from an image
def extract_content(image, colour=const.WHITE):
    size_x = image.width  // const.MENU_SIZE
    size_y = image.height // const.MENU_SIZE

    data = [[False for y in range(size_y)] for x in range(size_x)]
    for x in range(size_x):
        for y in range(size_y):
            if image.getpixel((x * const.MENU_SIZE, y * const.MENU_SIZE)) == colour:
                data[x][y] = True
    return data

'''
def matches_enchant(enchant, image):
    for x in range(120):
        for y in range(8):
            if enchant[x][y]:
                if image.getpixel((x * const.MENU_SIZE, y * const.MENU_SIZE)) != const.TEXT_GREY:
                    return False
    return True
'''

# check to see if a enchanted book should be kept
def check_book():
    pydirectinput.move(1, 1)
    pydirectinput.moveTo(*const.MOUSE_2)
    image = ImageGrab.grab(const.TRADE_2.BOX)
    # check if the book is desired
    enchant = extract_content(image, GREY) # max length of enchat is 120

    if (enchant in const.WANTS):
        return True
    print_data(enchant)
    return False

# check to see if the price is right
def check_price():
    # check if price is desired

    # extract_content(image, (80, 55), (12, 7), WHITE)
    return True

# check the villager for any trade that are wanted
def check_villager():
    return check_book() and check_price()
