from . import layouts
import tkinter as tk
from PIL import ImageTk, Image
import os

CWD = "%s" % os.getcwd()
DEFAULT_ARROW_SRC = "gui\\images\\arrow_triangle.png"

class IncrementPanel(layouts.Layout):
    # Note the arrow_src should point to an image file with an UPWARDS pointing arrow
    def __init__(self, master, increment_function, decrement_function, arrow_src=DEFAULT_ARROW_SRC):
        super().__init__(master)
        # Note that the increment is on the BOTTOM and decrement is on the TOP
        # This is because the upcs are listed top to bottom as indicies increase
        # Meaning that an increase in the index results in a graphically lower position in the list
        DEFAULT_HEIGHT = 30
        DEFAULT_WIDTH = DEFAULT_HEIGHT
        self.increment_button = tk.Button(self.widget, command=increment_function, width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT)
        self.increment_button.pack(side=tk.BOTTOM)
        self.decrement_button = tk.Button(self.widget, command=decrement_function, width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT)
        self.decrement_button.pack(side=tk.TOP)

        arrow_src_full_url = "%s\\%s" % (CWD, arrow_src)
        if os.path.exists(arrow_src_full_url):
            arrow_up = Image.open(arrow_src).resize((16,16))
            self.arrow_up_img = ImageTk.PhotoImage(arrow_up)
            self.arrow_down_img = ImageTk.PhotoImage(arrow_up.rotate(180))
            self.decrement_button.config(image=self.arrow_up_img)
            self.increment_button.config(image=self.arrow_down_img)
        else:
            self.decrement_button.config(text="^")
            self.increment_button.config(text="V")
