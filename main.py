from tkinter import *
import random
import pandas

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
dat = pandas.read_csv("data/french_words.csv")
print(dat.to_dict(orient="records"))
try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    words_to_learn = original_data.to_dict(orient="records")
else:
    words_to_learn = data.to_dict(orient="records")


# Translation

def translate():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")
    canvas.itemconfig(canvas_background, image=card_back_image)


# Next_card function

def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(words_to_learn)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    canvas.itemconfig(canvas_background, image=card_front_image)
    flip_timer = window.after(3000, translate)


def update_words():
    words_to_learn.remove(current_card)
    new_data = pandas.DataFrame(words_to_learn)
    new_data.to_csv("data/words_to_learn.csv", index=False)
    print(len(words_to_learn))
    next_card()


# Window
window = Tk()
window.title("Flash Cards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(1000, translate)

# Canvas
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_image = PhotoImage(file="images/card_front.png")
card_back_image = PhotoImage(file="images/card_back.png")
canvas_background = canvas.create_image(400, 263, image=card_front_image)
card_title = canvas.create_text(400, 135, text="", font=("Arial", 35, "normal"))
card_word = canvas.create_text(400, 280, text="", font=("Arial", 50, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

# x_button
x_image = PhotoImage(file="images/wrong.png")
x_button = Button(image=x_image, width=100, height=99, highlightthickness=0, bg=BACKGROUND_COLOR, command=next_card)
x_button.grid(row=1, column=0)

# y_button
y_image = PhotoImage(file="images/right.png")
y_button = Button(image=y_image, width=100, height=100, highlightthickness=0, bg=BACKGROUND_COLOR, command=update_words)
y_button.grid(row=1, column=1)

next_card()

window.mainloop()
