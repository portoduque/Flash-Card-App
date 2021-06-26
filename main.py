from tkinter import *
import random
from os import path
import pandas as pd

BACKGROUND_COLOR = "#B1DDC6"
current_card = []


def next_card():
    global flip_timer, current_card
    window.after_cancel(flip_timer)

    current_card = random.choice(data)
    english_word = current_card["English"]
    portuguese_word = current_card["Portuguese"]

    # Front Card
    canvas.itemconfig(card_background, image=card_front_img)
    canvas.itemconfig(card_title, text="Inglês", fill="black")
    canvas.itemconfig(card_word, text=english_word, fill="black")

    # Back Card
    flip_timer = window.after(3000, flip_card, portuguese_word)


def flip_card(portuguese_word):
    canvas.itemconfig(card_background, image=card_back_img)
    canvas.itemconfig(card_title, text="Português", fill="white")
    canvas.itemconfig(card_word, text=portuguese_word, fill="white")


def is_known():
    data.remove(current_card)

    new_data = pd.DataFrame(data, columns=["English", "Portuguese"])
    new_data.to_csv("data/words_to_learn.csv", index=False)

    next_card()


# ------------------------------ Data SETUP------------------------------ #
if path.exists("data/words_to_learn.csv"):
    df = pd.read_csv("data/words_to_learn.csv")
    data = df.to_dict(orient="records")
else:
    df = pd.read_csv("data/english_words.csv")
    data = df.to_dict(orient="records")


# ------------------------------ UI SETUP ------------------------------ #
window = Tk()
window.title("Flash Card")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

# Setup timer to flip the card.
flip_timer = window.after(3000, flip_card)

# Canvas
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
card_background = canvas.create_image(400, 263, image=card_front_img)


card_title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))  # Language text
card_word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))  # Word text

canvas.grid(column=0, row=0, columnspan=2)

# Button
check_img = PhotoImage(file="images/right.png")
known_button = Button(image=check_img, highlightthickness=0, command=is_known)
known_button.grid(column=1, row=1)

cross_img = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=cross_img, highlightthickness=0, command=next_card)
unknown_button.grid(column=0, row=1)

next_card()

window.mainloop()
