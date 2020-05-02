import os
import readline
import glob
from getch import getch
from tkinter import Tk
from tkinter.filedialog import askopenfilename


def choose_file(terminal, file_type, extension):
    if terminal:
        return choose_file_in_terminal(file_type, extension)
    return choose_file_in_file_chooser(file_type, extension)


def choose_file_in_terminal(file_type, extension):

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
        else:
            print('I did not find the "' + str(extension) + '" file at "' + user_input + '". Please try again!')

    return user_input


def file_chooser_error():
    while True:
        user_input = getch()
        if user_input == b'\x04':
            raise KeyboardInterrupt
        if user_input in (b'1', b'2'):
            return user_input


def choose_file_in_file_chooser(file_type, extension):
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
            print('1 - Try again')
            print('2 - Choose file in terminal')
            answer_file_chooser_error = file_chooser_error()
            print()
            if answer_file_chooser_error == b'2':
                return choose_file_in_terminal(file_type, extension)
        else:
            break
    return user_input
