from PIL import Image, ImageGrab

import time
import enchants

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
def extract_content(image, location, size, colour=(255, 255, 255)):
    data = [[False for x in range(size[1])] for y in range(size[0])]
    for x in range(size[0]):
        for y in range(size[1]):
            if image.getpixel((location[0] + 5 * x, location[1] + 5 * y)) == colour:
                data[x][y] = True
    return data

# check to see if a enchanted book should be kept
def check_book(image):
    # check if the book is desired
    enchant = extract_content(image, (490, 65), (120, 8), GREY) # max length of enchat is 120

    if (enchant in enchants.wanted):
        return True
    print_data(enchant)
    return False

# check to see if the price is right
def check_price():
    # check if price is desired

    # extract_content(image, (80, 55), (12, 7), WHITE)
    return True

# check the villager for any trade that are wanted
def check_villager(image):
    return check_book(image) and check_price()
