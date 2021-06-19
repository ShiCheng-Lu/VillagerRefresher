from PIL import Image, ImageGrab
# import mouse
import pydirectinput
import keyboard

import enchants
import const
import check_villager
import reset_villager
import setup

# get an image of the second trade slot

if __name__ == "__main__":
    enchants.want("efficiency")
    enchants.want("power")
    enchants.want("sharpness")

    # start set up and program when esc is pressed
    keyboard.wait('backspace')

    setup.setup_all()
    pydirectinput.press('e')
    while (True):
        reset_villager.reset_villager()

        if check_villager.check_villager():
            break
        pydirectinput.press('e')
        if keyboard.is_pressed('backspace'):
            quit()
