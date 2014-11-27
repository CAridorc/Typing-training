# -*- coding: utf-8 -*-
import sys
from subprocess import Popen, PIPE, STDOUT

if sys.version_info.major == 2:
    import Tkinter as tk
    import tkMessageBox as pop_up
    import tkFileDialog
else:
    import Tkinter as tk
    import tkinter.tkMessageBox as pop_up
    import tkinter.tkFileDialog as tkFileDialog


import datetime

import glob

import os


TXT_EXTENSION = ".txt"
ALL_CHARS = "abcdefghijklmnopqrstuvwxyz12345690"

EMPTY_TITLE_ERROR_MESSAGE_SAVE = "Please write the name of the file you want to save in the given field."
EMPTY_TITLE_ERROR_MESSAGE_OPEN = "Please write the name of the file you want to open in the given field."
FILE_NOT_FOUND_ERROR_MESSAGE = "No file with the given title was found, remember that this text editor can only read files in its directory."
INVALID_CHARACTERS_MESSAGE = "Unicode does not allow accented letters, please replace them in the following way: è -> e', à -> a'."
SIGNATURE_TXT_NOT_FOUND_MESSAGE = "Please be sure that the file you want to open exists and that it is in the same folder of this editor."
SAVING_SUCCESS_MESSAGE = "Your text is now stored in the {filename} file"

NO_ERROR = ('', None)


def _open():
    filename = tkFileDialog.askopenfilename()
    file_title.delete(0, tk.END)
    file_title.insert(tk.INSERT, filename)
    with open(filename) as f:
            main_text.delete("1.0", tk.END)
            main_text.insert(tk.INSERT, f.read(), "a")


def save(alert=True):
    if not file_title.get():
        pop_up.showerror("No title.", EMPTY_TITLE_ERROR_MESSAGE_SAVE)
        return False
    
    try:
        title = file_title.get()
    except UnicodeEncodeError:
        pop_up.showerror("Invalid characters",INVALID_CHRACTERS_MESSAGE)
        return False
        
    filename = title    
    
    with open(filename, "w+") as f:
        try:
            f.write(main_text.get(1.0, tk.END))
        except UnicodeEncodeError:
            pop_up.showerror("Invalid characters",INVALID_CHARACTERS_MESSAGE)
            return False
        
        try:
            if alert:
                pop_up.showinfo("File saved succesfully.",
SAVING_SUCCESS_MESSAGE.format(filename=filename))
        except UnicodeEncodeError:
            pop_up.showerror("Invalid characters",INVALID_CHARACTERS_MESSAGE)


def exec_bash(shell_command):
    event = Popen(shell_command, shell=True, stdin=PIPE, stdout=PIPE, 
    stderr=STDOUT)
    return event.communicate()

def compile_(filename,flags,optimization="-O3"):
    command = "gcc " + filename + " " + optimization +" " + flags
    return exec_bash(command)

def execute(filename="a.out"):
    return exec_bash("./"+filename)

def get_flags():
    text = main_text.get(1.0, tk.END)
    flags = ""
    if "FLAGS" in text:
        lines = text.splitlines()
        line1 = lines[0]
        line1 = line1.replace("// FLAGS","")
        flags = line1
        flags = flags.replace("// FLAGS","")
    return flags

def run():
    save(alert=False)
    filename = file_title.get()
    flags = get_flags()
    result = compile_(filename,flags)
    if result == NO_ERROR:
        pop_up.showinfo("The output is: ",execute())
    else:
            pop_up.showinfo("Error found when compiling",result)

root = tk.Tk()
root.wm_title("C ide")

menubar = tk.Menu(root)
menubar.add_command(label="Open", command=_open)
menubar.add_command(label="Save", command=save)
menubar.add_command(label="Run", command=run)

root.config(menu=menubar)

top = tk.Frame(root)
temp = tk.Label(root, text="Title:")
temp.pack(in_=top, side=tk.LEFT)

file_title = tk.Entry(root)
file_title.pack(in_=top, side=tk.RIGHT)

top.pack()

main_text = tk.Text(root)
main_text.pack()

tk.mainloop()
