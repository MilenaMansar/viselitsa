import sys
from tkinter import *
import random

root = Tk()
root.title("Виселица")
root.geometry("800x600")

if sys.platform == "darwin":
    root.lift()
    root.call('wm', 'attributes', '.', '-topmost', '1')
    root.after_idle(root.call, 'wm', 'attributes', '.', '-topmost', '0')

c = Canvas(root, width=800, height=600)
c.pack()

word = ""
symbols = []
mistakes = 0
guessed = []

def cross():
    c.delete("all")
    y = 0
    while y < 600:
        x = 0
        while x < 800:
            c.create_rectangle(x, y, x+75, y+55, fill="white", outline="black")
            x = x+75
        y = y+55

rules = '''
Правила игры "Виселица"

Цель игры: Угадать название факультета МФТИ, 
скрытое за рядом подчеркиваний.

Ход игры:

1. Начало игры: Компьютер выбирает случайное название факультета МФТИ
2. Отображение: На экране отображается виселица и ряд подчеркиваний, 
соответствующих количеству букв в загаданном слове.
3. Ввод букв: Игрок вводит с клавиатуры букву.
4. Проверка:
  * Если введенная буква присутствует в слове, то она открывается 
  на соответствующем месте в скрытом слове. 
  * Если введенная буква отсутствует в слове, то к виселице 
  добавляется одна часть тела (голова, туловище, руки, ноги).
5. Попытки: Игрок имеет 6 попыток, чтобы угадать слово. 
6. Победа: Если игрок угадывает слово, он побеждает.
7. Поражение: Если игрок исчерпывает все 6 попыток, не угадав слово, он проигрывает.

Удачи!
'''

c.create_text(400, 250, text=rules, fill="black", font=('Helvetica', "14"), width=700)

words = ["Мфти", "Вшпи", "Фпми", "Фртк", "Фопф", "Фэфм", "Фбвт", "Фбмф"]

def start():
    global word, symbols, guessed, mistakes, text_items
    word = random.choice(words).upper()
    symbols = ['_' for _ in word]
    guessed = []
    mistakes = 0
    draw_gallows()
    
    text_items = []
    x_start = 450
    for i, symbol in enumerate(symbols):
        item = c.create_text(x_start + i * 60, 160, text=symbol, fill="black", font=("Helvetica", "50"))
        text_items.append(item)

    root.bind("<Key>", on_key_press)

def draw_gallows():
    c.create_line(100, 500, 100, 100, width=5)
    c.create_line(100, 100, 300, 100, width=5)
    c.create_line(300, 100, 300, 150, width=5)

def on_key_press(event):
    global mistakes
    letter = event.char.upper()

    if not letter.isalpha() or len(letter) != 1:
        return

    if letter in guessed:
        return

    guessed.append(letter)

    if letter in word:
        for i, char in enumerate(word):
            if char == letter:
                symbols[i] = letter
                c.itemconfig(text_items[i], text=letter)

        if "_" not in symbols:
            end_game("Вы победили!", "green", "40")
    else:
        mistakes += 1
        draw_hangman(mistakes)

        if mistakes == 6:
            end_game(f"Вы проиграли! Слово было: {word}", "red", "20")

def draw_hangman(mistakes):
    if mistakes == 1:
        c.create_oval(250, 150, 350, 250, width=5)
    elif mistakes == 2:
        c.create_line(300, 250, 300, 400, width=5)
    elif mistakes == 3:
        c.create_line(300, 300, 250, 350, width=5)
    elif mistakes == 4:
        c.create_line(300, 300, 350, 350, width=5)
    elif mistakes == 5:
        c.create_line(300, 400, 250, 500, width=5)
    elif mistakes == 6:
        c.create_line(300, 400, 350, 500, width=5)

def end_game(message, color, font_size):
    c.create_text(400, 300, text=message, fill=color, font=("Helvetica", font_size), width=700)
    root.unbind("<Key>")

    restart_btn = Button(root, text="Играть заново", command=lambda: [cross(), start(), restart_btn.destroy()])
    restart_btn.place(relx=0.5, rely=0.7, anchor=CENTER)
    restart_btn["bg"] = "#4CAF50"
    restart_btn["fg"] = "white"
    restart_btn["font"] = ("Helvetica", 16)

def start_screen():
    c.create_text(400, 250, text=rules, fill="black", font=('Helvetica', "14"), width=700)

    bttn1 = Button(root, text="Начать игру", command=lambda: [cross(), start(), bttn1.destroy()])
    bttn1.place(relx=0.5, rely=0.7, anchor=CENTER)
    bttn1["bg"] = "red"
    bttn1["fg"] = "white"
    bttn1["font"] = ("Helvetica", 16)

start_screen()
root.mainloop()
