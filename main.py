from PIL import Image, ImageGrab, ImageFilter
import pygetwindow
import keyboard
import pydirectinput

import numpy as np

def crop(image, bounds):
    x_start, y_start, x_end, y_end = bounds
    return image[y_start:y_end, x_start:x_end]

def find_bounds(image, threshold=0.01):
    x_range = np.mean(image, axis=0) > threshold
    y_range = np.mean(image, axis=1) > threshold

    x_start, x_end = -1, 0
    y_start, y_end = -1, 0

    for i, c in enumerate(x_range):
        if c:
            if x_start == -1:
                x_start = i
            x_end = i

    for i, c in enumerate(y_range):
        if c:
            if y_start == -1:
                y_start = i
            y_end = i
    
    return x_start, y_start, x_end + 1, y_end + 1

def colour_filter(image, colour):
    return (image == colour).all(axis=2)

DIALOGUE_BOX_COLOUR = (198, 198, 198)

def move_to_trade():
    image = np.array(ImageGrab.grab())

    image = colour_filter(image, DIALOGUE_BOX_COLOUR)
    x_start, y_start, x_end, y_end = find_bounds(image)
    if x_start == -1 or y_start == -1:
        return False

    trade_location_x = 0.7 * x_start + 0.3 * x_end
    trade_location_y = 0.7 * y_start + 0.3 * y_end

    pydirectinput.moveTo(int(trade_location_x), int(trade_location_y))
    pydirectinput.moveTo(int(trade_location_x), int(trade_location_y) + 1)
    return True

ITEM_BACKGROUND_COLOUR = (27, 12, 27)
TEXT_COLOUR = (197, 197, 197)

def check_trade():
    image = np.array(ImageGrab.grab())
    # get the image output of the enchantment book
    item_filter = colour_filter(image, ITEM_BACKGROUND_COLOUR)
    image = crop(image, find_bounds(item_filter))
    text_filter = colour_filter(image, TEXT_COLOUR)
    text = crop(text_filter, find_bounds(text_filter))

    # not an enchanted book trade
    if text.shape[0] == 0:
        return False

    # compare with desired books
    for enchantment in desired_enchantments:
        if compare(text, enchantments[enchantment]):
            return True
    return False

import math
def compare(image, target):
    # first, find out scale factor of image
    scale = math.ceil(image.shape[0] / target.shape[0])
    scaled_image = image[::scale, ::scale]

    return scaled_image.shape == target.shape and (scaled_image == target).all()

import os
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
    # print(enchantments.keys())

desired_enchantments = ["mending"]

running = True
def terminator(key):
    global running
    if key.name == "backspace":
        running = False
import time
def main():
    keyboard.hook(terminator)

    load_enchantments()
    keyboard.wait('/')
    
    while running:
        if (check_trade()):
            keyboard.wait("/")
        
        # refresh villager
        pydirectinput.press("e")
        time.sleep(0.2)
        pydirectinput.press('space')
        while running and not move_to_trade():
            pydirectinput.click(button='right')
            time.sleep(0.2)

if __name__ == "__main__":
    main()