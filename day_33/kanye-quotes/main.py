# Import the GUI toolkit and the HTTP library used to fetch Kanye quotes.
from tkinter import *
import requests


# Fetch a fresh quote from the Kanye REST API and update the text on the canvas.
def get_quote():
    respond = requests.get("https://api.kanye.rest")
    respond.raise_for_status()
    quote = respond.json()["quote"]
    canvas.itemconfig(quote_text, text=quote)


# Create the main application window and set its basic spacing and title.
window = Tk()
window.title("Kanye Says...")
window.config(padx=50, pady=50)

# Draw the canvas that holds the background image and the quote text.
canvas = Canvas(width=300, height=414)
background_img = PhotoImage(file="background.png")
canvas.create_image(150, 207, image=background_img)
quote_text = canvas.create_text(
    150, 207, text="Kanye Quote Goes HERE", width=250, font=("Arial", 30, "bold"), fill="white"
)
canvas.grid(row=0, column=0)

# Add the Kanye image button that triggers a new quote when clicked.
kanye_img = PhotoImage(file="kanye.png")
kanye_button = Button(image=kanye_img, highlightthickness=0, command=get_quote)
kanye_button.grid(row=1, column=0)


# Start the Tkinter event loop so the window stays open and responsive.
window.mainloop()
