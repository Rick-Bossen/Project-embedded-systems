from tkinter import ttk

BACKGROUND_COLOR = '#765d69'
FRAME_COLOR = '#989C60'


def style_init(window):
    style = ttk.Style()

    # Window style
    window.configure(background=BACKGROUND_COLOR, padx=25, pady=25)
    window.state('zoomed')

    style.theme_create('custom', 'default', settings={
        ".": {
            "configure": {"foreground": "white", "background": FRAME_COLOR, "font": "Doppio 14", "highlightthickness": 0}
        },
        "TNotebook": {
            "configure": {"background": BACKGROUND_COLOR}
        },
        "TNotebook.Tab": {
            "configure": {"padding": [20, 5], "background": FRAME_COLOR, "bordercolor": FRAME_COLOR, "highlightthickness": 0, "lightcolor": FRAME_COLOR}
        }
    })
    style.theme_use('custom')
    window.style = style

