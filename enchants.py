from PIL import Image, ImageGrab

import const

# add an enchantment to the wanted list
# stop refreshing the villager when an enchantment from the wanted list occurs
def want(enchant):
    image = Image.open("enchants/" + enchant + ".png")
    data = [[False for y in range(8)] for x in range(120)]

    for x in range(120):
        for y in range(8):
            if image.getpixel((x, y)) == const.TEXT_GREY:
                data[x][y] = True
    
    const.WANTS.append(data)
