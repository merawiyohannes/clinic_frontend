# style/themes.py

from .colors import *
from .fonts import *


def style_button(widget):
    widget.config(
        bg=BUTTON_BG,
        fg=BUTTON_FG,
        activebackground="#357ABD",
        activeforeground="#ffffff",
        relief="sunken",
        bd=0
    )

def style_label(widget):
    widget.config(
        bg=BACKGROUND
    )

def style_entry(widget):
    widget.config(
        font=ENTRY_FONT,
        bg=ENTRY_BG,
        highlightbackground=ENTRY_BORDER,
        highlightcolor=ENTRY_BORDER,
        highlightthickness=1,
        relief="solid",
        bd=0
    )
