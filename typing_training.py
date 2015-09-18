try:
    import tkinter as tk
except:
    import Tkinter as tk
import random
import urllib.request

FONT = font=(None, 50)

try:
    with open("/usr/share/dict/words") as f:
        words = f.read().splitlines()
except IOError:
    with open("/usr/share/dict/words", "w+") as f:
        f.write(urllib.request.urlopen("https://raw.githubusercontent.com/eneko/data-repository/master/data/words.txt").read().decode())
                
new_word = lambda: random.choice(words)

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
