import glob
import os
from tkinter import Tk
from tkinter.filedialog import askopenfilename

import readline

from constants import OPTION_ONE, OPTION_TWO, OPTION_CANCEL, INTERRUPT, TEXT_OPTION_ONE, TEXT_OPTION_TWO, \
    TEXT_OPTION_CANCEL
from getch import getch


def choose_file(terminal, file_type, extension, default=None):
    if terminal:
        return choose_file_in_terminal(file_type, extension, default)
    return choose_file_in_file_chooser(file_type, extension, default)


def choose_file_in_terminal(file_type, extension, default=None):

    def complete(text, state):
        return (glob.glob(text+'*')+[None])[state]

    while True:
        readline.set_completer_delims(' \t\n;')
        readline.parse_and_bind('tab: complete')
        readline.set_completer(complete)
        user_input = input('Path to ' + file_type + ' file (' + extension + '): ')

        if os.path.isfile(user_input) and user_input.lower().endswith(extension):
            print()
            break
        elif user_input == ':q':
            print()
            return default
        else:
            print('I did not find the "' + str(extension) + '" file at "' + user_input +
                  '". Please try again! (:q to use the other option)')

    return user_input


def file_chooser_error():
    while True:
        user_input = getch()
        if user_input == INTERRUPT:
            raise KeyboardInterrupt
        if user_input in (OPTION_ONE, OPTION_TWO, OPTION_CANCEL):
            return user_input


def choose_file_in_file_chooser(file_type, extension, default=None):
    dialog_title = 'Choose "' + file_type + '" file'
    file_extensions = [(file_type, extension)]
    initial_directory = './'
    while True:
        window = Tk()
        window.withdraw()
        user_input = askopenfilename(title=dialog_title, initialdir=initial_directory, filetypes=file_extensions)
        window.destroy()
        if user_input == '':
            print('No file chosen. What would you like to do?')
            print(TEXT_OPTION_ONE + ' - Try again')
            print(TEXT_OPTION_TWO + ' - Choose file in terminal')
            print(TEXT_OPTION_CANCEL + ' - Cancel and use the other option')
            answer_file_chooser_error = file_chooser_error()
            print()
            if answer_file_chooser_error == OPTION_TWO:
                return choose_file_in_terminal(file_type, extension)
            if answer_file_chooser_error == OPTION_CANCEL:
                return default
        else:
            break
    return user_input
