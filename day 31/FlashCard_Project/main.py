import random
from tkinter import *

import pandas as pd

# ---------- App styling ----------
# These colors and settings keep the flashcards visually consistent.
BACKGROUND_COLOR = "#b1ddc6"
FRONT_COLOR = "white"
BACK_COLOR = "#9BC1B0"
FONT_COLOR = "black"
SET_TIMER = 5
LEARNING_LANGUAGE = "Deutsch"
MOTHER_LANGUAGE = "Magyar"

# ---------- Data loading ----------
# Try to load the personalized word list first.
# If it does not exist yet, fall back to the default vocabulary file.
try:
    dataset = pd.read_csv(f"data/{LEARNING_LANGUAGE}_words_to_learn.csv")
except FileNotFoundError:
    dataset = pd.read_csv("data/ger_hun_pl.csv")

# Convert the CSV data into a list of dictionaries so each card is easy to access.
dictionary = dataset.to_dict(orient="records")

# This variable stores the currently running timer callback.
timer = None


# ---------- Card logic ----------
# Show the back of the card and the translated word.
def flip_card():
    # Re-enable the answer buttons when the card is flipped.
    button_ok.config(text="", state="normal")
    button_x.config(state="normal")

    # Switch the card image to the backside.
    card_canvas.itemconfig(card_img, image=card_back_img)

    # Update the text to the other language.
    title_label.config(text=MOTHER_LANGUAGE, bg=BACK_COLOR, fg=FONT_COLOR)
    word_label.config(text=current_card[MOTHER_LANGUAGE], bg=BACK_COLOR, fg=FONT_COLOR)


# Pick a random word and show the front side of the card.
def new_card():
    global current_card

    # Cancel the previous countdown so it does not continue after a new card appears.
    if timer is not None:
        window.after_cancel(timer)

    # Disable the buttons until the user has decided whether they knew the word.
    button_ok.config(state="disabled")
    button_x.config(state="disabled")

    # Choose a random card from the current study list.
    current_card = random.choice(dictionary)

    # Reset the UI to the front side of the card.
    card_canvas.itemconfig(card_img, image=card_front_img)
    title_label.config(
        text=LEARNING_LANGUAGE,
        font=("Arial", 40, "italic"),
        bg=FRONT_COLOR,
        fg=FONT_COLOR,
    )
    word_label.config(
        text=current_card[LEARNING_LANGUAGE],
        wraplength=600,
        font=("times new roman", 50, "bold"),
        bg=FRONT_COLOR,
        fg=FONT_COLOR,
    )

    # Start the countdown for this card.
    countdown(SET_TIMER)


# Save the word as learned and remove it from the active study list.
def save():
    # Remove the card from the list of words still to learn.
    dictionary.remove(current_card)

    # Save the updated list back to the CSV file.
    pd.DataFrame(dictionary).to_csv(
        f"data/{LEARNING_LANGUAGE}_words_to_learn.csv", index=False
    )

    # Move to the next card immediately.
    new_card()


# Count down from the set timer and flip the card once time is up.
def countdown(time):
    global timer

    if time > 0:
        # Schedule the next second tick.
        timer = window.after(1000, countdown, time - 1)

        # Show the remaining seconds on the OK button.
        button_ok.config(
            text=time,
            font=("times new roman", 30, "bold"),
            disabledforeground=FONT_COLOR,
        )
    else:
        # When time runs out, reveal the answer.
        flip_card()


# ---------------------------- UI SETUP ------------------------------- #
# Build the main window and all visible flashcard elements.
window = Tk()
window.title("FlashCard")
window.config(width=900, height=700, background=BACKGROUND_COLOR, padx=50, pady=50)

# ---------- Card area ----------
# Create the canvas that displays the front/back of the flashcard.
card_canvas = Canvas(
    window, width=800, height=530, bg=BACKGROUND_COLOR, highlightthickness=0
)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
card_img = card_canvas.create_image(400, 265, image=card_front_img)
card_canvas.grid(row=0, column=0, columnspan=2, pady=50)

# Labels are placed on top of the card to show the language name and the word.
title_label = Label()
title_label.place(in_=card_canvas, x=400, y=150, anchor="center")

word_label = Label()
word_label.place(in_=card_canvas, x=400, y=305, anchor="center")

# ---------- Action buttons ----------
# Wrong answer: move to the next card without saving the word.
button_x_img = PhotoImage(file="images/wrong.png")
button_x = Button(
    image=button_x_img,
    highlightbackground=BACKGROUND_COLOR,
    borderwidth=0,
    relief="flat",
    command=new_card,
)
button_x.grid(row=1, column=0, pady=50)

# Right answer: mark the word as learned and remove it from the study set.
button_ok_img = PhotoImage(file="images/right.png")
button_ok = Button(
    image=button_ok_img,
    bg=BACKGROUND_COLOR,
    highlightthickness=0,
    bd=0,
    compound="center",
    command=save,
)
button_ok.grid(row=1, column=1, pady=50)

# Start the first flashcard as soon as the app opens.
new_card()

window.update_idletasks()
window.mainloop()
