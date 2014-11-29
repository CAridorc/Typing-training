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

import platform

WINDOWS_ENDING = ".exe"
LINUX_ENDING = ".out"

EMPTY_TITLE_ERROR_MESSAGE_SAVE = "Please write the name of the file you want to save in the given field."
EMPTY_TITLE_ERROR_MESSAGE_OPEN = "Please write the name of the file you want to open in the given field."
INVALID_CHARACTERS_MESSAGE = "Unicode does not allow accented letters, please replace them in the following way: è -> e', à -> a'."
SAVING_SUCCESS_MESSAGE = "Your text is now stored in the {filename} file"

NO_ERROR = ('', None)


def replace_old_title(new_title):
    """
    Replace the old content of the widget
    file_title with a new title.
    """
    file_title.delete(0, tk.END)
    file_title.insert(tk.INSERT, new_title)


def replace_old_text(new_text):
    """
    Replace the old content of the widget
    main_text with a new title.
    """
    main_text.delete("1.0", tk.END)
    main_text.insert(tk.INSERT, new_text, "a")


def open_():
    """
    Opens a file using the built-in file explorer,
    and displays its text in the main text field.
    """
    filename = tkFileDialog.askopenfilename()
    replace_old_title(filename)
    with open(filename) as f:
        replace_old_text(f.read())


def title_is_empty():
    """
    Return True if the tite is empty.
    """
    return not file_title.get()


def invalid_characters_in_title():
    """
    Handles invalid characters in the
    title widget. Mainly accented letters.
    """
    try:
        __ = file_title.get()
    except UnicodeEncodeError:
        return True


def invalid_characters_in_body():
    """
    Handles invalid characters in the
    title widget. Mainly accented letters.
    """
    try:
        f.write(main_text.get(1.0, tk.END))
    except UnicodeEncodeError:
        return True


def save(alert=True):
    """
    Saves the content of the main text widget into a file,
    handles any kind of error that may happen.
    If alert is True: showes a pop up message to inform the user if
    the file is saved successfuly.
    """
    if title_is_empty():
        pop_up.showerror("No title.", EMPTY_TITLE_ERROR_MESSAGE_SAVE)
        return False

    if invalid_characters_in_title():
        pop_up.showerror("Invalid characters", INVALID_CHARACTERS_MESSAGE)
        return False

    filename = file_title.get()

    with open(filename, "w+") as f:
        try:
            f.write(main_text.get(1.0, tk.END))
        except UnicodeEncodeError:
            pop_up.showerror("Invalid characters", INVALID_CHARACTERS_MESSAGE)
            return False
        if alert:
            try:
                pop_up.showinfo("File saved succesfully.",
                                SAVING_SUCCESS_MESSAGE.format(filename=filename))
            except UnicodeEncodeError:
                pop_up.showerror(
                    "Invalid characters",
                    INVALID_CHARACTERS_MESSAGE)


def exec_bash(shell_command):
    """
    Runs a shell_command.
    Taken from http://stackoverflow.com/questions/4256107/running-bash-commands-in-python
    User contributions are licensed under cc by-sa 3.0 with attribution required.
    """
    event = Popen(shell_command, shell=True, stdin=PIPE, stdout=PIPE,
                  stderr=STDOUT)
    return event.communicate()


def compile_(filename, flags):
    """
    Uses the gcc compiler to compile the file.
    """
    command = "gcc " + filename + " " + flags
    return exec_bash(command)


def system_is(name):
    """
    Returns True if the os is equal to the given name.
    >>> system_is("Linux")
    True # If you are on linux
    False # If you are on Windows or Mac
    """
    operating_system = platform.system()
    if operating_system == name:
        return True


def decide_ending():
    """
    Decides the correct ending of the executable file
    basing on the os.
    """
    if system_is("Windows"):
        return WINDOWS_ENDING
    elif system_is("Linux"):
        return LINUX_ENDING


def nice_format_for_execute(result):
    """
    The second argument is always going to be None,
    I only care about the first one
    """
    return result[0]


def execute(filename="a"):
    """
    Executes the "a" executable taking care that
    the ending is correct.
    Format the result before outputting it.
    """
    filename += decide_ending()
    result = exec_bash("./" + filename)
    result = nice_format_for_execute(result)
    return result


def delete(string, sub_string):
    """
    Returns the string without the sub_string chars.
    >>> delete("Hello, how are you?","Hello, ")
    how are you?
    """
    string = string.replace(sub_string, "")
    return string


def get_flags():
    """
    Gets eventual compiler flags.
    Flags must be in the first line of the file,
    in the following format:
    // FLAGS -myflag1 -myflag2
    """
    flags = ""
    text = main_text.get(1.0, tk.END)
    flags = ""
    lines = text.splitlines()
    first_line = lines[0]
    if "// FLAGS" in first_line:
        flags += delete(first_line, "// FLAGS")
    return flags


def run():
    """
    Runs the file.
    If there is a compile time error it is shown. #TODO format compile errrors
    Otherwise, if the compilation is successful the result
    is shown in a pop up.
    """
    save(alert=False)
    filename = file_title.get()
    flags = get_flags()
    result = compile_(filename, flags)
    if result == NO_ERROR:
        pop_up.showinfo("The output is: ", execute())
    else:
        pop_up.showinfo("Error found when compiling", result)


# Here the GUI code starts.
root = tk.Tk()
root.wm_title("C ide")


menubar = tk.Menu(root)
menubar.add_command(label="Open", command=open_)
menubar.add_command(label="Save", command=save)
menubar.add_command(label="Run", command=run)
root.config(menu=menubar)


top = tk.Frame(root)
tk.Label(root, text="Title:").pack(in_=top, side=tk.LEFT)
file_title = tk.Entry(root)
file_title.pack(in_=top, side=tk.RIGHT)
top.pack()


main_text = tk.Text(root)
main_text.pack(expand=True, fill='both')

tk.mainloop()
