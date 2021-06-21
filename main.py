from PIL import Image, ImageGrab
# import mouse
import pydirectinput
import keyboard
import time

import enchants
import const
import check_villager
import reset_villager
import setup


def start_trade_sequence():
    pydirectinput.click(button='right')
    time.sleep(0.2)
    setup.setup_all()
    pydirectinput.press('e')
    while (True):
        reset_villager.reset_villager()

        if check_villager.check_villager():
            break
        pydirectinput.press('e')
        if keyboard.is_pressed('backspace'):
            break

def main():
    while True:
        keyboard.wait('/')
        parse = keyboard.get_typed_strings(keyboard.record('enter'))
        args = next(parse).split(' ')
        if args[0] == "autotrade" and len(args) >= 1:
            const.WANTS = []
            const.WANTS_STR = []
            for i in range(1, len(args)):
                try:
                    enchants.want(args[i])
                except:
                    pass
            time.sleep(0.1)
            if len(const.WANTS) >= 0:
                start_trade_sequence()

if __name__ == "__main__":
    main()
