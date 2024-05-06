from tkinter import *
import math
import random

# ---------------------------- CONSTANTS ------------------------------- #
FONT_NAME = "Courier"
MIN = 0.10
timer = None
timer_started = False  # Flag to check if timer has started
selected_text = None


# ---------------------------- Random INPUT TEXT ------------------------------- #

def select_random_text():
    global selected_text
    with open("sample_text.txt", mode="r") as f:
        texts = f.readlines()
        selected_text = random.choice(texts).lower()
    return selected_text


# ---------------------------- TAKING THE INPUT ------------------------------- #

# Function to continuously capture input
def capture_input(event):
    global timer_started
    user_input = input_text.get("1.0", END)
    # You can process the input here

    with open("input.txt", mode="w") as f:
        f.write(user_input)
    # Start the timer on the first key press
    if not timer_started:
        start_timer()
        timer_started = True

    highlight_correct_words(user_input)


# ---------------------------- TIMING FUNCTIONALITY ------------------------------- #

def start_timer():
    work_sec = MIN * 60
    count_down(work_sec)


def count_down(count):
    global timer
    # Stop the timer if it reaches zero
    if count <= 0:
        time_left_label.config(text="Time's up!")
        calculate_results()
        input_label.config(state=DISABLED)
        return
    else:
        time_left_label.config(text=f"Time left: {count}")
        timer = window.after(1000, count_down, count - 1)


# ---------------------------- Calculate Result ------------------------------- #
def calculate_results():
    global selected_text
    user_input = input_text.get("1.0", "end-1c").strip().lower()
    user_words = user_input.split()
    sample_words = selected_text.strip().lower().split()

    # Calculate words per minute (WPM)
    wpm = len([word for word in user_words if word in sample_words[:len(user_words)]]) / MIN
    wpm_label.config(text=f"WPM: {wpm:.2f}")


# ---------------------------- Highlight Correct Words ------------------------------- #
def highlight_correct_words(user_input):
    global selected_text
    user_input = input_text.get("1.0", "end-1c").strip().lower()
    user_words = user_input.split()
    sample_words = selected_text.strip().lower().split()

    # Clear previous tags
    sample_text.tag_remove("correct", "1.0", END)

    # Initialize index for sample text
    sample_index = "1.0"
    for word in sample_words[:len(user_words)]:
        # Find the end index of the current word
        end_index = sample_text.search(word, sample_index, stopindex=END)
        if end_index:
            # Calculate the end position based on the length of the word
            end_pos = f"{end_index}+{len(word)}c"
            # Check if the word is in the user's input
            if word in user_words:
                # Highlight the word
                sample_text.tag_add("correct", end_index, end_pos)
            # Update the start index for the next word
            sample_index = end_pos
        else:
            break  # Break the loop if no more words are found

    # Update the sample text to show correct words in green
    sample_text.tag_config("correct", foreground="green")


# ---------------------------- RESTART ------------------------------- #
def restart():
    global timer_started, selected_text, timer
    # Stop the current timer
    if timer:
        window.after_cancel(timer)
    timer_started = False

    # Clear the input text
    input_text.delete("1.0", END)

    # Re-enable the input field if it was disabled
    input_label.config(state=NORMAL)

    # Reset the timer label
    time_left_label.config(text="Time left: 60")

    # Select a new random text
    selected_text = select_random_text()
    sample_text.config(state=NORMAL)
    sample_text.delete("1.0", END)
    sample_text.insert(END, selected_text)
    sample_text.config(state=DISABLED)

    # Reset the WPM label
    wpm_label.config(text="WPM: ? ")

    # Remove any previous highlights
    sample_text.tag_remove("correct", "1.0", END)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Typing Speed Test")

title_label = Label(text="Typing Speed", font=(FONT_NAME, 30))
title_label.grid(column=1, row=0)

canvas = Canvas(width=1000, height=600, highlightthickness=0)
canvas.grid(column=1, row=1)

# information's
wpm_label = Label(canvas, text="WPM: ? ", width=10, font=(FONT_NAME, 11, "bold"))
wpm_label.place(x=280, y=40)

time_left_label = Label(canvas, text="Time left: 60", width=15, font=(FONT_NAME, 11, "bold"))
time_left_label.place(x=390, y=40)

restart_button = Button(canvas, text="Restart", width=8, font=(FONT_NAME, 10, "bold"), command=restart)
restart_button.place(x=600, y=38)

# Sample Text
entry_label = Label(canvas, text="Sample Text:", width=15, font=(FONT_NAME, 11, "bold"))
entry_label.place(x=140, y=70)

sample_text = Text(canvas, height=15, width=60, font=(FONT_NAME, 10, "bold"))
sample_text.insert(END, select_random_text())
sample_text.config(state=DISABLED)
sample_text.tag_configure("correct", foreground="black")  # Add tag for correct words
sample_text_window = canvas.create_window(100, 80, window=sample_text)
sample_text.place(x=280, y=70)

# Input Text
input_label = Label(canvas, text="Input Text:", width=15, font=(FONT_NAME, 11, "bold"))
input_label.place(x=140, y=320)

input_text = Text(canvas, height=15, width=60)
input_text.focus()
input_text.insert(END, "")
input_text_window = canvas.create_window(100, 80, window=input_text)
input_text.place(x=280, y=320)

# Bind the Text widget to the function that captures input
input_text.bind("<KeyRelease>", capture_input)

window.mainloop()

# TODO 5: 1 dakika bittiğinde sonuçları ekrana ver
# TODO 6: yeniden başlatma için restart butonunu ekle ve yapıyı oluştur
