import click
import random
import re
import colorama
from colorama import Fore, Back, Style

# Init libraries
colorama.init()


# Intialize game
def init_game():
    welcome_message = """Hello friend, this is a "Hangman" game.\n
    Guess letters and enjoy!"""
    welcome_hint = Fore.CYAN + '\nTip: type "exit" to quit game\n' + Style.RESET_ALL
    print(welcome_message + welcome_hint)
    game()
    return True


# Main function of game
def game():
    game_end = False
    word_list = ["hangman", "game", "tinkoff", "fintech", "programmer"]
    word_count = len(word_list) - 1
    word_guessed = word_list[random.randint(0, word_count)]
    word_length = len(word_guessed)
    word_show = ["*" for x in range(word_length)]
    word_guessed_count = 0
    letter_list_already_guessed = []
    attempts_initial = 5
    attempts = attempts_initial

    # Start the main part of programm
    while game_end is False:
        print(''.join(word_show))
        new_letter = input_word('', letter_list_already_guessed)
        letters_position = letter_positions_in_string(word_guessed, new_letter)
        if letters_position != []:
            print('Hit!')
            for j in letters_position:
                word_show[j] = new_letter
                word_guessed_count = word_guessed_count + 1
        else:
            attempts = attempts - 1
            print('Missed, you have', attempts, 'attempts out of ', attempts_initial)
        game_result = check_game_end(word_guessed_count, word_length, attempts)
        if game_result != 'continue':
            closing_game(game_result, word_guessed)


# End of game
def closing_game(game_result, word_guessed):
    print('Game ended')
    if game_result == 'win':
        print('Congratulations! You guessed the word: ', word_guessed)
    else:
        print('Sorry, you loose')
    print('would you like to play another Hangman? y/n', '\n')
    input_letter = input()
    if input_letter == 'y':
        init_game()
    if input_letter == 'n':
        print('Goodbye!')
    if input_letter not in ['y', 'n']:
        exit()


# Check if we should stop the game or not
def check_game_end(word_guessed_count, word_length, attempts):
    game_result = 'continue'
    if word_guessed_count >= word_length:
        game_result = 'win'
    if attempts <= 0:
        game_result = 'loose'
    return game_result


# Check if user hit right letter in guessed word
def letter_positions_in_string(word_guessed, letter):
    result = list()
    word_length = len(word_guessed)
    for i in range(word_length):
        if (word_guessed[i] == letter):
            # print('type of result is ',type(result))
            # print('i = ',i)
            result.append(i)
    # print('return = ',result)
    return result


# User input
def input_word(input_string, letter_list_already_guessed):
    end = False
    test_stop = 0
    while ((end is False) and (test_stop <= 1)):
        if input_string == '':
            string = input('Guess a letter: ')
            letter = ''.join(string)
            end = is_letter_correct(letter, letter_list_already_guessed)
        else:
            test_stop = test_stop + 1
            string = input_string
            letter = ''.join(string)
            end = is_letter_correct(letter, letter_list_already_guessed)
            return end
    return string


# Work with incorrect input
def is_letter_correct(letter, letter_list_already_guessed):
    is_correct = True
    # global letter_list_already_guessed
    error_message = ''
    if letter in letter_list_already_guessed:
        is_correct = False
        error_message = 'You have already check this letter!!! Please enter new'
    else:
        if len(letter) > 1:
            is_correct = False
            error_message = 'You write more than 1 letter, pls enter single letter'
        if len(letter) <= 0:
            is_correct = False
            error_message = 'You enter empty data, pls print single letter'
        if len(letter) == 1 and len(re.findall(r'[a-z]', letter)) == 0:
            is_correct = False
            error_message = 'You enter non-latin or CAPS latter, pls use proper litera'
        if letter == 'exit':
            print('abort game')
            exit()
    if is_correct is False:
        print(error_message)
    if is_correct is True:
        letter_list_already_guessed.append(letter)
    return is_correct


if __name__ == '__main__':
    init_game()
