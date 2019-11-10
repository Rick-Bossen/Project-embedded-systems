from enum import Enum
from tkinter.ttk import Style


# class that contains all style and theme data
class Theme:

    WIDTH = 900
    HEIGHT = 480
    SIZE = (WIDTH, HEIGHT)

    PADDING = 10

    TK_NB_WIDTH = WIDTH * .87
    TK_DATA_BUTTON_WIDTH = WIDTH * .13

    ROW_HEIGHT = 34
    COLUMN_WIDTH = TK_NB_WIDTH / 4

    R_ICO = r'resources/sun.ico'

    FONT_FAMILY = 'Roboto'
    FONT = FONT_FAMILY + ' 11'
    FONT_LARGE = FONT_FAMILY + ' 14'
    FONT_COLOR = '#ffffff'

    BACKGROUND_COLOR = '#2F4F4F'
    DISABLED_COLOR = '#AEC3B0'
    FRAME_COLOR = '#598392'
    HIGHLIGHT_COLOR = '#EF5B5B'

    # Object styling
    BUTTON = {'background': HIGHLIGHT_COLOR, 'foreground': FONT_COLOR, 'font': FONT}
    LABEL_HEADER = {'background': FRAME_COLOR, 'foreground': FONT_COLOR, 'font': FONT_LARGE}
    LABEL = {'background': FRAME_COLOR, 'foreground': FONT_COLOR, 'font': FONT}

    @staticmethod
    def init():
        style = Style()
        style.theme_create('notebook', settings={
            "TNotebook": {"configure": {"background": Theme.BACKGROUND_COLOR}},
            "TNotebook.Tab": {
                "configure": {"padding": [5, 1], "background": Theme.DISABLED_COLOR, 'foreground': Theme.FONT_COLOR},
                "map": {"background": [("selected", Theme.FRAME_COLOR)],
                        "foreground": [("selected", Theme.FONT_COLOR), ("active", Theme.HIGHLIGHT_COLOR)]}
            }
        })
        style.theme_use('notebook')
