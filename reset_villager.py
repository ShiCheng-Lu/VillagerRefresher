from PIL import Image, ImageGrab

import pydirectinput
import time

in_trade_image = Image.open("in_trade.png")

top = 684
left = 1794
width = 52
height = 2

# check if the trading menu is opened
def in_trade():
    image = ImageGrab.grab(bbox=(left, top, left + width, top + height))
    # compare the two image
    for x in range(52):
        for y in range(2):
            if (in_trade_image.getpixel((x, y)) != image.getpixel((x, y))):
                return False
    return True

# wait until the villager get a job
def wait_for_job():
    while (not in_trade()):
        pydirectinput.click(button='right')
        time.sleep(0.2)

# remove the villager's job
def remove_job():
    pydirectinput.press('space') 

# remove the villager's job and gives it a new one
def reset_villager():
    remove_job()
    time.sleep(1) 
    wait_for_job()
