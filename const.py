
class _ScreenBox:
    LEFT = None
    RIGHT = None
    TOP = None
    BOTTOM = None

    WIDTH = None
    HEIGHT = None
    BOX = None

    def set_attr(self):
        if (self.LEFT and self.RIGHT and self.TOP and self.BOTTOM):
            self.BOX = (self.LEFT, self.TOP, self.RIGHT, self.BOTTOM)
            self.WIDTH = self.RIGHT - self.LEFT
            self.HEIGHT = self.BOTTOM - self.TOP
            return True
        else:
            return False

SETUP_COMPLETE = False
# game bounds
GAME = _ScreenBox()
# menu bounds
MENU = _ScreenBox()
MIN_MENU_WIDTH = 316
MENU_SIZE = 1
# menu_check
MENU_CHECK = _ScreenBox()
# second trade
MOUSE_2 = None
TRADE_2 = _ScreenBox()
PRICE_2 = _ScreenBox()

# colour
BLACK       = (0, 0, 0)
TEXT_GREY   = (170, 170, 170)
GREY        = (170, 170, 170)
WHITE       = (255, 255, 255)

# enchants
WANTS = []
