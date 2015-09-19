try:import tkinter as tk
except:import Tkinter as tk
import random

FONT = font=(None, 50)
WORDS = ['the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'I', 'it', 'for', 'not', 'on', 'with',
         'he', 'as', 'you', 'do', 'at', 'this', 'but', 'his', 'by', 'from', 'they', 'we', 'say', 'her',
         'she', 'or', 'an', 'will', 'my', 'one', 'all', 'would', 'there', 'their', 'what', 'so', 'up',
         'out', 'if', 'about', 'who', 'get', 'which', 'go', 'me', 'when', 'make', 'can', 'like', 'time',
         'no', 'just', 'him', 'know', 'take', 'people', 'into', 'year', 'your', 'good', 'some', 'could',
         'them', 'see', 'other', 'than', 'then', 'now', 'look', 'only', 'come', 'its', 'over', 'think',
         'also', 'back', 'after', 'use', 'two', 'how', 'our', 'work', 'first', 'well', 'way', 'even',
         'new', 'want', 'because', 'any', 'these', 'give', 'day', 'most', 'us']

def new_word():
    # Pareto principle, the top 10 words are used much more than to words from 10 -> 100, so I show them more often.
    word = random.choice(random.choice((WORDS[0:len(WORDS)//10], WORDS)))
    return new_word() if word == text_to_copy.cget("text") else word

root = tk.Tk()
root.title("Typing trainer")

text_to_copy = tk.Label(root, text = "start", font=FONT)
text_to_copy.pack()

typing_ground = tk.Entry(root, font=FONT)
typing_ground.pack()

points = tk.Label(root, text = "Score: 0", font=FONT)
points.pack()

def if_equal_delete_and_take_other_phrase(ev):
    if text_to_copy.cget("text") == typing_ground.get():
        typing_ground.delete(0, 'end')
        text_to_copy['text'] = new_word()
        points['text'] = "Score: " + str(int(points['text'].split(': ')[-1]) + 1)
        
root.bind('<Key>', if_equal_delete_and_take_other_phrase)

root.mainloop()
