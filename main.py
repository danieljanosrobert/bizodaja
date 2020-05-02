import file_chooser
from getch import getch

one = option_linear_algorithm = b'1'
two = option_neural_network = b'2'
change_file_chooser_option = b'7'
interrupt = b'\x04'
path_database = './tsaasraining.1600000.processed.noemoticon.csv'


def change_answer(answer):
    return two if answer == one else one


def choose_file(file_type, extension):
    is_terminal = answer_file_choosing_option == one
    return file_chooser.choose_file(is_terminal, file_type, extension)


def wait_for_byte(condition):
    global answer_file_choosing_option
    while True:
        user_input = getch()
        if user_input == interrupt:
            raise KeyboardInterrupt
        elif change_file_chooser_option in condition and user_input == change_file_chooser_option:
            answer_file_choosing_option = change_answer(answer_file_choosing_option)
            print('File chooser option changed to ' +
                  ('terminal.' if answer_file_choosing_option == one else 'file chooser'))
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
print('1 - Terminal')
print('2 - File chooser')
print('If you choose "File chooser" the chooser window may appear behind the terminal')
answer_file_choosing_option = wait_for_byte([one, two])

print('Would you like to use something else instead of the default dataset?')
print('1 - Yes, I would rather use a personal sentiment database')
print('2 - No, the default is OK')
print('7 - Change file chooser option')
answer_specific_datababse = wait_for_byte([one, two, change_file_chooser_option])
if answer_specific_datababse == one:
    path_database = choose_file('database as csv', '.csv')

print('Which model would you use?')
print('1 - Linear Algorithm')
print('2 - Neural Network')
answer_chosen_model = wait_for_byte([option_linear_algorithm, option_neural_network])

print('Would you like to use a saved model?')
print('1 - Yes')
print('2 - No, I would like to create a new one')
print('7 - Change file chooser option')
answer_saved_model = wait_for_byte([one, two, change_file_chooser_option])
if answer_saved_model == one:
    path_saved_model = choose_file('model', '.la' if answer_chosen_model == option_linear_algorithm else '.nn')
    if answer_chosen_model == option_neural_network:
        path_tfidf = choose_file('tfidf', '.tfidf')

#TODO: Call model and do the stuff.