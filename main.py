import sys

import env
import file_chooser
from constants import *
from evaluation import evaluate_from_report
from getch import getch
from model import init_model

path_database = './training.1600000.processed.noemoticon.csv'
path_saved_model = None
path_tfidf = None


def change_answer(answer):
    return OPTION_TWO if answer == OPTION_ONE else OPTION_ONE


def choose_file(file_type, extension, default=None):
    is_terminal = answer_file_choosing_option == OPTION_ONE
    return file_chooser.choose_file(is_terminal, file_type, extension, default)


def wait_for_byte(condition):
    global answer_file_choosing_option
    while True:
        user_input = getch()
        if user_input == INTERRUPT:
            raise KeyboardInterrupt
        elif OPTION_CHANGE_CHOOSING_METHOD in condition and user_input == OPTION_CHANGE_CHOOSING_METHOD:
            answer_file_choosing_option = change_answer(answer_file_choosing_option)
            print('File chooser option changed to ' +
                  ('terminal.' if answer_file_choosing_option == OPTION_ONE else 'file chooser'))
            continue
        elif user_input in condition:
            print()
            break
    return user_input


print('██████╗ ██╗███████╗ ██████╗ ██████╗  █████╗      ██╗ █████╗')
print('██╔══██╗██║╚══███╔╝██╔═══██╗██╔══██╗██╔══██╗     ██║██╔══██╗')
print('██████╔╝██║  ███╔╝ ██║   ██║██║  ██║███████║     ██║███████║')
print('██╔══██╗██║ ███╔╝  ██║   ██║██║  ██║██╔══██║██   ██║██╔══██║')
print('██████╔╝██║███████╗╚██████╔╝██████╔╝██║  ██║╚█████╔╝██║  ██║')
print('╚═════╝ ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝ ╚════╝ ╚═╝  ╚═╝')
print('Welcome! Would you like to use terminal, or File chooser to choose files?')
print(TEXT_OPTION_ONE + ' - Terminal')
print(TEXT_OPTION_TWO + ' - File chooser')
print('If you choose "File chooser" the chooser window may appear behind the terminal')
answer_file_choosing_option = wait_for_byte([OPTION_ONE, OPTION_TWO])

print('Would you like to use something else instead of the default dataset?')
print(TEXT_YES + ' - Yes (with ["label", "id", "date", "flag", "user", "text"] columns and no header)')
print(TEXT_NO + ' - No, the default is OK')
print(TEXT_OPTION_EVALUATE + ' - Just evaluate an existing report')
print(TEXT_OPTION_CHANGE_CHOOSING_METHOD + ' - Change file chooser option')
answer_specific_datababse = wait_for_byte([YES, NO, OPTION_EVALUATE, OPTION_CHANGE_CHOOSING_METHOD])
if answer_specific_datababse == YES:
    path_database = choose_file('database as' + EXTENSION_DATASET, EXTENSION_DATASET, default=path_database)
elif answer_specific_datababse == OPTION_EVALUATE:
    evaluate_from_report(choose_file('report', EXTENSION_REPORT))
    sys.exit()

print('Would you like to use stopwords?')
print(TEXT_YES + ' - Yes')
print(TEXT_NO + ' - No')
env.STOPWORDS = True if wait_for_byte([YES, NO]) == YES else False

print('Which model would you use?')
print(TEXT_OPTION_LOGR + ' - Logistic Regression')
print(TEXT_OPTION_NN + ' - Neural Network')
print(TEXT_OPTION_SGD + ' - SGD Classifier (baseline)')
answer_chosen_model = wait_for_byte([OPTION_LOGR, OPTION_NN, OPTION_SGD])

print('Would you like to use a saved model?')
print(TEXT_YES + ' - Yes')
print(TEXT_NO + ' - No, I would like to create a new one')
print(TEXT_OPTION_CHANGE_CHOOSING_METHOD + ' - Change file chooser option')
answer_saved_model = wait_for_byte([YES, NO, OPTION_CHANGE_CHOOSING_METHOD])
if answer_saved_model == OPTION_ONE:
    path_saved_model = choose_file('model', EXTENSION_LOGR if answer_chosen_model == OPTION_LOGR else (EXTENSION_NN if answer_chosen_model == OPTION_NN else EXTENSION_SGD))
    if path_saved_model:
        path_tfidf = choose_file('tfidf', EXTENSION_TFIDF)

init_model(path_database, answer_chosen_model, path_saved_model, path_tfidf)
