from . import layouts
import tkinter as tk


class IncrementPanel(layouts.Layout):
    def __init__(self, master, increment_function, decrement_function, arrow_src=None):
        super().__init__(master)
        # Note that the increment is on the BOTTOM and decrement is on the TOP
        # This is because the upcs are listed top to bottom as indicies increase
        # Meaning that an increase in the index results in a graphically lower position in the list

        self.increment_button = tk.Button(self.widget, command=increment_function)
        self.increment_button.pack(side=tk.BOTTOM)
        self.decrement_button = tk.Button(self.widget, command=decrement_function)
        self.decrement_button.pack(side=tk.TOP)
