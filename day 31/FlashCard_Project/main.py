from tkinter import *

import pandas as pd

BACKGROUND_COLOR = "#428361"

# ---------------------------- UI SETUP ------------------------------- #
# WINDOW - Main application window configuration

window = Tk()
window.title("FlashCard")
window.config(width=900, height=700, background= BACKGROUND_COLOR, padx=50, pady=50)

card_canvas= Canvas(window, width=800, height=525, background= 'red')
card_canvas.pack()




window.update_idletasks()
window.mainloop()



