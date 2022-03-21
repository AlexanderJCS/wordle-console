# Import packages
import random
from string import ascii_lowercase

from read_file import read_file

import enchant
from colorama import Fore, init

init(autoreset=True)
d = enchant.Dict("en_US")

# Read config file
SOLUTION_FILE = "solution_words.json"
SETTINGS_FILE = "settings.json"

settings = read_file(SETTINGS_FILE)

try:
    WIDTH = settings["board_width"]
    HEIGHT = settings["board_height"]
except KeyError:
    input(f"Invalid key for {SOLUTION_FILE}. Press enter to close. ")
    exit()

EMPTY = "—"


# Class game
class Game:
    def __init__(self, solution_words_dict):
        self.board = [[EMPTY for _ in range(WIDTH)] for _ in range(HEIGHT)]

        try:
            if WIDTH > 1:
                self.solution_word = random.choice(solution_words_dict[str(WIDTH)])
            else:
                self.solution_word = random.choice(ascii_lowercase)

        except KeyError:
            input(f"Invalid key for {SOLUTION_FILE}. Is the width correct? Press enter to close. ")
            exit()

        self.correct_places = set()
        self.incorrect_places = set()
        self.wrong_letter = set()

    def run_game(self):
        # Logic of the game
        while True:
            self.print_board()
            self.print_letters()
            self.input_word()

            # Check if won
            if won := self.win_check() is not None:
                if not won:
                    self.print_board()
                    print(f"{Fore.RED}You lose!\n"*3)
                self.share()
                print(f"The word was {self.solution_word}")
                break

    def input_word(self):
        while True:
            # Allow the user to input a word
            user_word = input("Enter a word: ").lower()

            # Check if the word is valid
            if len(user_word) != WIDTH:
                print(f"{Fore.RED}Incorrect length")
                continue

            if not d.check(user_word):
                print(f"{Fore.RED}Not a real word")
                continue

            if list(user_word) in self.board:
                print(f"{Fore.RED}Word already given")
                continue
            break

        # Put user's guess in board
        for i, word in enumerate(self.board):
            if word[0] == EMPTY:
                self.board[i] = list(user_word)
                break

    def print_board(self):  # Print the board
        print()

        for word in self.board:
            solution_word_list = list(self.solution_word)

            for i, letter in enumerate(word):
                if letter in solution_word_list:
                    if solution_word_list[i] == letter:  # If the letter is in the correct place
                        self.correct_places.add(letter)

                        if letter in self.incorrect_places:
                            self.incorrect_places.remove(letter)

                        color_fore = Fore.GREEN

                    else:  # If the letter is in an incorrect place but it is in the final word
                        if letter not in self.correct_places:
                            self.incorrect_places.add(letter)

                        color_fore = Fore.YELLOW

                    for x in range(len(solution_word_list)):  # Remove letter from the solution word list
                        if solution_word_list[x] == letter:
                            solution_word_list[x] = ""
                            break

                else:  # If the letter is not in the final word
                    self.wrong_letter.add(letter)
                    color_fore = ""

                print(f'{color_fore}{word[i]}', end=" ")  # Print the letter
            print()

    def print_letters(self):
        # Print correct, incorrect, and wrong letters
        for letter in ascii_lowercase:
            color = ""
            if letter in self.correct_places:
                color = Fore.GREEN

            elif letter in self.incorrect_places:
                color = Fore.YELLOW

            elif letter in self.wrong_letter:
                color = Fore.RED

            print(f"{color}{letter.upper()}", end=" ")
        print()

    def win_check(self):
        for word in self.board:
            solution_list = list(self.solution_word)

            if word == solution_list:
                self.print_board()
                print(f"{Fore.GREEN}You win!\n"*3)
                return True

        return False if self.board[-1][-1] != EMPTY else None

    def share(self):
        print("Shareable emojis:")
        for word in self.board:
            if word[0] == EMPTY:
                break

            for i, solution_letter in enumerate(self.solution_word):
                letter = word[i]

                if solution_letter == letter:
                    print("\N{Large Green Square}", end="")

                elif letter in self.solution_word:
                    print("\N{Large Yellow Square}", end="")

                else:
                    print("\N{Black Large Square}", end="")
            print()


# Functions
def main():
    solution_words = read_file(SOLUTION_FILE)

    while True:
        g = Game(solution_words)
        g.run_game()


if __name__ == "__main__":
    main()
