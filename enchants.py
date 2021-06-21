from PIL import Image, ImageGrab

import const

class Enchantment():
    def __init__(self, name, level):
        this.name = name
        this.level = level

# add an enchantment to the wanted list
# stop refreshing the villager when an enchantment from the wanted list occurs
def want(enchant):
    if enchant in const.WANTS_STR:
        return
    
    image = Image.open("enchants/" + enchant + ".png")
    data = [[False for y in range(8)] for x in range(120)]

    for x in range(120):
        for y in range(8):
            if image.getpixel((x, y)) == const.TEXT_GREY:
                data[x][y] = True
    
    const.WANTS_STR.append(enchant)
    const.WANTS.append(data)
