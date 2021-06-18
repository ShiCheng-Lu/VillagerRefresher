from PIL import Image, ImageGrab
# import mouse
import pyautogui
import pydirectinput
import time
import keyboard

import enchants
import check_villager
import reset_villager

top = 875
left = 1200
width = 1100
height = 110

# get an image of the second trade slot
def get_image():
    time.sleep(0.1)
    pydirectinput.moveTo(1600, 920)
    pydirectinput.moveTo(1620, 920)

    return ImageGrab.grab(bbox=(left, top, left + width, top + height))

running = True

enchants.want("efficiency")

time.sleep(3)
while (running):
    reset_villager.reset_villager()
    image = get_image()

    if check_villager.check_villager(image):
        break
    pydirectinput.press('e')

    if keyboard.is_pressed('backspace'):
        break
