from PIL import Image, ImageGrab
import keyboard
import pydirectinput
import time

import const

menu_check_img = Image.open("menu_imgs/menu_check.png")

# check if the trading menu is opened
def in_trade():
    image = ImageGrab.grab(const.MENU_CHECK.BOX)
    # compare the two image
    for x in range(4):
        for y in range(4):
            if (menu_check_img.getpixel((x, y)) != image.getpixel((x * const.MENU_SIZE, y * const.MENU_SIZE,))):
                return False
    return True

# wait until the villager get a job
def wait_for_job():
    while (not in_trade()):
        pydirectinput.click(button='right')

# remove the villager's job
def remove_job():
    pydirectinput.press('space') 

# remove the villager's job and gives it a new one
def reset_villager():
    remove_job()
    time.sleep(1) 
    wait_for_job()
