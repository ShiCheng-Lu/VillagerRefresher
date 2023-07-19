import time
import math
import os
from PIL import Image, ImageGrab
import keyboard
import pydirectinput
import numpy as np
import time
import pygetwindow

best_enchantments = {
    # "aqua_affinity": 5,
    "bane_of_arthropods": 17,
    "blast_protection": 14,
    "channeling": 5,
    # "depth_strider": 11,
    # "efficiency": 17,
    # "feather_falling": 14,
    "fire_aspect": 8,
    "fire_protection": 14,
    "flame": 5,
    # "fortune": 11,
    # "frost_walker": 16,
    "impaling": 17,
    "infinity": 5,
    "knockback": 8,
    "looting": 11,
    "loyalty": 11,
    "luck_of_the_sea": 11,
    "lure": 11,
    # "mending": 10,
    "multishot": 11,
    # "piercing": 14,
    "power": 17,
    # "projectile_protection": 14,
    "protection": 14,
    # "punch": 8,
    "quick_charge": 11,
    "respiration": 11,
    # "riptide": 11,
    # "sharpness": 17,
    # "silk_touch": 5,
    "smite": 17,
    # "thorns": 11,
    "unbreaking": 11,
}

best_enchantments = {
    # "aqua_affinity": 5,
    # "bane_of_arthropods": 17,
    # "blast_protection": 14,
    # "channeling": 5,
    # "depth_strider": 11,
    # "efficiency": 17,
    # "feather_falling": 14,
    # "fire_aspect": 8,
    # "fire_protection": 14,
    # "flame": 5,
    # "fortune": 11,
    # "frost_walker": 16,
    "impaling": 17,
    # "infinity": 5,
    # "knockback": 8,
    # "looting": 11,
    # "loyalty": 11,
    # "luck_of_the_sea": 11,
    # "lure": 11,
    # "mending": 10,
    # "multishot": 11,
    # "piercing": 14,
    "power": 17,
    # "projectile_protection": 14,
    "protection": 14,
    # "punch": 8,
    # "quick_charge": 11,
    # "respiration": 11,
    # "riptide": 11,
    "sharpness": 17,
    # "silk_touch": 5,
    # "smite": 17,
    # "thorns": 11,
    "unbreaking": 11,
}

# desired_enchantments = {
#     "mending": 10
# }
desired_enchantments = best_enchantments

DIALOG_BOX_COLOUR = (198, 198, 198)
ITEM_BACKGROUND_COLOUR = (27, 12, 27)
TEXT_COLOUR = (197, 197, 197)
PRICE_TEXT_COLOUR = (255, 255, 255)

def crop(image, bounds):
    x_start, y_start, x_end, y_end = bounds
    return image[y_start:y_end, x_start:x_end]


def find_bounds(image, threshold=0.01):
    x_start, x_end = -1, 0
    y_start, y_end = -1, 0

    for x in np.where(np.mean(image, axis=0) > threshold)[0]:
        if x_start == -1:
            x_start = x
        x_end = x

    for y in np.where(np.mean(image, axis=1) > threshold)[0]:
        if y_start == -1:
            y_start = y
        y_end = y

    return x_start, y_start, x_end + 1, y_end + 1

def colour_filter(image, colour):
    return (image == colour).all(axis=2)

def move_mouse(x, y):
    '''
    move mouse to a relative location in game
    '''
    pydirectinput.moveTo(x + window_mask[0], y + window_mask[1])
    

def move_to_trade():
    image = np.array(ImageGrab.grab(window_mask))

    image = colour_filter(image, DIALOG_BOX_COLOUR)
    x_start, y_start, x_end, y_end = find_bounds(image)
    if x_start == -1 or y_start == -1:
        return False

    # second trade slot
    trade_location_x = (215/310) * x_start + (95/310) * x_end
    trade_location_y = 0.7 * y_start + 0.3 * y_end

    move_mouse(int(trade_location_x) + 5, int(trade_location_y))
    move_mouse(int(trade_location_x), int(trade_location_y))
    return True


def check_enchant(image):
    # get the image output of the enchantment book
    item_filter = colour_filter(image, ITEM_BACKGROUND_COLOUR)
    image = crop(image, find_bounds(item_filter))
    text_filter = colour_filter(image, TEXT_COLOUR)
    text = crop(text_filter, find_bounds(text_filter))

    # not an enchanted book trade
    if text.shape[0] == 0:
        return None

    # compare with desired books
    for enchantment in desired_enchantments.keys():
        if compare(text, enchantments[enchantment]):
            return enchantment
    return None


def compare(image, target):
    # first, find out scale factor of image
    scale = math.ceil(image.shape[0] / target.shape[0])
    scaled_image = image[::scale, ::scale]

    return scaled_image.shape == target.shape and (scaled_image == target).all()


def check_price(image):
    dialog_image = colour_filter(image, DIALOG_BOX_COLOUR)
    x_start, y_start, x_end, y_end = find_bounds(dialog_image)
    if x_start == -1 or y_start == -1:
        return False

    bounds = (
        int((295/310) * x_start + (15/310) * x_end),
        int((110/160) * y_start + (50/160) * y_end),
        int((265/310) * x_start + (45/310) * x_end),
        int((100/160) * y_start + (60/160) * y_end),
    )
    image = crop(image, bounds)
    price_image = colour_filter(image, PRICE_TEXT_COLOUR)
    price_image = crop(price_image, find_bounds(price_image, 0))
    # scale to 7 high
    scale = price_image.shape[0] // 7
    price_image = price_image[::scale, ::scale]

    price_string = "0"

    for x in range(price_image.shape[1] - 4):
        res = (price_image[:, x:x + 5] == prices).all(axis=(1, 2))
        if res.any():
            price_string += str(np.argmax(res))

    return int(price_string)


def check_trade():
    image = np.array(ImageGrab.grab(window_mask))

    enchant = check_enchant(image)
    if enchant == None:
        return False

    price = check_price(image)
    return price <= desired_enchantments[enchant]


enchantments = {}


def load_enchantments():
    for file in os.listdir("./enchants"):
        enchantment_name = os.path.splitext(file)[0]
        file_path = os.path.join("./enchants", file)
        image = np.array(Image.open(file_path))
        # old text is different coloured
        text_filter = 1 - colour_filter(image, ITEM_BACKGROUND_COLOUR)
        image = crop(text_filter, find_bounds(text_filter, threshold=0))
        enchantments[enchantment_name] = image

prices = []


def load_prices():
    global prices

    file_path = "./price.png"
    image = np.array(Image.open(file_path))
    # print(image.shape)
    image = colour_filter(image, PRICE_TEXT_COLOUR)

    for i in range(10):
        prices.append(image[:, 6 * i: 6 * (i + 1) - 1])
    prices = np.array(prices)
    # print(prices)


running = True
window_mask = None

def load_window_mask(title):
    global window_mask

    for window in pygetwindow.getWindowsWithTitle(title):
        if (window.title != title):
            continue

        window_mask = [
            window.left + 50,
            window.top + 50,
            window.right - 50,
            window.bottom - 50
        ]
        return

def terminator(key):
    global running
    if key.name == "backspace":
        running = False


def main():
    global window_mask

    keyboard.hook(terminator)

    load_enchantments()
    load_prices()
    keyboard.wait('/')
    
    window_mask = None
    while window_mask == None:
        load_window_mask("Minecraft")
        time.sleep(1)

    while running:
        if check_trade():
            keyboard.wait("/")

        # refresh villager
        pydirectinput.press("e")
        pydirectinput.press('space')
        
        window_mask = None
        while window_mask == None:
            load_window_mask("Minecraft")
            time.sleep(0.5)

        while running and not move_to_trade():
            pydirectinput.click(button='right')
            time.sleep(0.5)


if __name__ == "__main__":
    main()
