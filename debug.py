
from main import *

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

    Image.fromarray(price_image).show()

    price_string = "0"

    for x in range(price_image.shape[1] - 4):
        res = (price_image[:, x:x + 5] == prices).all(axis=(1, 2))
        if res.any():
            price_string += str(np.argmax(res))

    return int(price_string)


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

window_mask = None

def load_window_mask(title):
    global window_mask

    for window in pygetwindow.getWindowsWithTitle(title):
        if (window.title != title):
            continue
        print([
            window.left,
            window.top,
            window.right,
            window.bottom
        ])
        window_mask = [
            window.left + 50,
            window.top + 50,
            window.right - 50,
            window.bottom - 50
        ]
        return

def move_to_trade():
    global window_mask
    image = np.array(ImageGrab.grab(window_mask))

    image = colour_filter(image, DIALOG_BOX_COLOUR)

    Image.fromarray(image).show()

    # x_start, y_start, x_end, y_end = find_bounds(image)
    # if x_start == -1 or y_start == -1:
    #     return False

    # # second trade slot
    # trade_location_x = (215/310) * x_start + (95/310) * x_end
    # trade_location_y = 0.7 * y_start + 0.3 * y_end

    # move_mouse(int(trade_location_x) + 5, int(trade_location_y))
    # move_mouse(int(trade_location_x), int(trade_location_y))
    # return True



# window_mask = None
load_prices()
load_window_mask("Minecraft")
print(window_mask)
print(move_to_trade())
