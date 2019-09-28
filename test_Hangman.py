import unittest
import Hangman
import numpy


class Test_Hangman(unittest.TestCase):

    def test_letter_positions_in_string(self):
        test_letters = numpy.array(['a', 'b', 'asd', 'r'])
        correct_answer = numpy.array([[0, 3], [], [], [4]])
        for i in range(4):
            self.assertEqual(correct_answer[i],
            Hangman.letter_positions_in_string('anvar', test_letters[i]))

    def test_input_word(self):
        test_letters = numpy.array(['fas', '6', 'F', ' ',
        'a', 'n', 'v', 'r', 'v'])
        letter_list_already_guessed = numpy.array([[''], [''], [''], [''],
        ['a'], ['a', 'v', 'c', 'y'], ['a'], ['a'], ['a', 'n', 'v', 'r']])
        correct_answer = numpy.array([False, False, False, False,
        False, True, True, True, False])
        for i in range(9):
            self.assertEqual(correct_answer[i],
            Hangman.input_word(test_letters[i], letter_list_already_guessed[i]))

    def test_is_letter_correct(self):
        test_letters = numpy.array(['fas', '6', 'F', ' ',
        'a', 'n', 'v', 'r', 'v'])
        letter_list_already_guessed = numpy.array([[''], [''], [''], [''],
        ['a'], ['a', 'v', 'c', 'y'], ['a'], ['a'], ['a', 'n', 'v', 'r']])
        correct_answer = numpy.array([False, False, False, False,
        False, True, True, True, False])
        for i in range(9):
            self.assertEqual(correct_answer[i],
            Hangman.is_letter_correct(test_letters[i], letter_list_already_guessed[i]))

    def test_check_game_end(self):
        test_word_guessed_count = numpy.array([1, 4, 2, 1, 6, 10, 11, -3, 9, 2])
        test_word_length = numpy.array([2, 12, 3, 5, 3, 2, 11, 10, 0, 1])
        test_attempts = numpy.array([5, 2, 0, -2, 4, 1, 0, 2, 3, 1])
        test_answers = numpy.array(['continue', 'continue', 'loose', 'loose',
        'win', 'win', 'loose', 'continue', 'win', 'win'])
        for i in range(9):
            self.assertEqual(test_answers[i],
            Hangman.check_game_end(test_word_guessed_count[i], test_word_length[i], test_attempts[i]))


if __name__ == '__main__':
    unittest.main()
