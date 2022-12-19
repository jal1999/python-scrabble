import constants
from random import choice, randint
from english_words import english_words_lower_alpha_set


class Scrabble:
    def __init__(self):
        self._letter_points = constants.POINTS
        self._hand: dict[str, int] = self._gen_starting_hand()
        self._score = 0
        self._english_words = [word.upper() for word in list(english_words_lower_alpha_set) if len(word) > 1]
        self.play_game()


    def _gen_starting_hand(self) -> dict[str, int]:
        """
        Generates the starting hand of the player.

        :return: starting hand of the player
        :rtype: dict[str, int]
        """
        starting_hand: dict[str, int] = {}
        for _ in range(constants.HAND_SIZE - 1):
            rand_letter = choice(constants.ALPHABET)
            starting_hand[rand_letter] = starting_hand.get(rand_letter, 0) + 1
        starting_hand['*'] = 1
        return starting_hand

    def _update_hand(self, hand: dict[str, int], word: str) -> None:
        """
        Updates the hand of the player after they have guessed a word

        :param hand: the dict of strings representing the letters the player
        can use
        :type hand: dict[str, int]
        :param word: the word the player guessed
        :type word: str
        :return: None
        """
        for char in word:
            if hand.get(char.upper(), 0) > 1:
                hand[char] -= 1
            else:
                del hand[char.upper()]

    def _is_valid_word(self, word: str) -> bool:
        """
        Determines if the user's guess is a valid guess

        :param word: the word the player guessed
        :return: True if their guess is valid, False otherwise
        :rtype: bool
        """
        new_word: str = ""
        for char in word:
            if char != '*':
                char = char.upper()
            new_word += char
        word = new_word
        if '*' not in word:
            for i, w in enumerate(self._english_words):
                if w == word:
                    return True
            return False
        else:
            return self._valid_word_wildcard(word.upper())

    def _valid_word_wildcard(self, word: str, idx=0) -> bool:
        """
        Helper function that determines if a word containing
        a wildcard is a valid guess

        :param word: the word the player guessed (containing a wildcard)
        :param idx: reusable index for where '*' is located in the original guess
        :return: True if the guess is valid, False otherwise
        :rtype: bool
        """
        if word.find('*') == -1:
            return word in self._english_words
        else:
            for vowel in constants.VOWELS:
                idx = word.find('*')
                word = word[:idx] + vowel + word[idx + 1:]
                if self._valid_word_wildcard(word, idx):
                    return True
                word = word[:idx] + '*' + word[idx + 1:]
            return False

    def get_score(self, n: int, word: str) -> int:
        """
        Computes the score of a given word

        :param n: number of letters available to the player
        :param word: the player's guess
        :return: computes score of the player's guess
        """
        letter_score: int = self._compute_letter_score(word)
        word_len_score: int = self._get_len_score(n, word)
        return letter_score * word_len_score

    def _compute_letter_score(self, word: str) -> int:
        """
        Computes the sum of each letter's score

        :param word: the player's guess
        :return: computes score of the player's guess
        """
        letter_score = 0
        for char in word:
            if char != '*':
                letter_score += self._letter_points[char.upper()]
        return letter_score

    def _get_len_score(self, n: int, word: str) -> int:
        """
        Computes the second component of a word's core

        :param n: number of letters available to the player
        :param word: the player's guess
        :return: computes score of the player's guess
        """
        first_choice: int = 7 * len(word) - 3 * (n - len(word))
        return max(first_choice, 1)

    def play_hand(self) -> str:
        """
        Playes a single hand

        :return: the player's valid input
        :rtype: str
        """
        print("Current hand:", end=" ")
        for (i, char) in enumerate(self._hand):
            if i == len(self._hand) - 1:
                print(char)
            else:
                if self._hand[char] > 1:
                    print(char, char, end=' ')
                else:
                    print(char, end=' ')
        word = input("Enter a word or \"!!\" to indicate you are finished: ")
        while not self._is_valid_word(word):
            if word == "!!":
                return ""
            word = input("That is not a valid word, please try a different one: ")
        score: int = self.get_score(len(self._hand), word)
        self._update_hand(self._hand, word)
        self._score += score
        print(f"\"{word}\" earned {score} points. Total score: {self._score}\n")
        return word

    def play_game(self):
        """
        Allow a user to play Scrabble
        :return: None
        """
        while self.play_hand() != "" and len(self._hand) != 0:
            pass
        print("Thanks for playing!")
