# The Word Game

import random
import string

VOWELS = "aeiou"
CONSONANTS = "bcdfghjklmnpqrstvwxyz"
HAND_SIZE = 15

SCRABBLE_LETTER_VALUES = {
    "a": 1,
    "b": 3,
    "c": 3,
    "d": 2,
    "e": 1,
    "f": 4,
    "g": 2,
    "h": 4,
    "i": 1,
    "j": 8,
    "k": 5,
    "l": 1,
    "m": 3,
    "n": 1,
    "o": 1,
    "p": 3,
    "q": 10,
    "r": 1,
    "s": 1,
    "t": 1,
    "u": 1,
    "v": 4,
    "w": 4,
    "x": 8,
    "y": 4,
    "z": 10,
}

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)

import os

WORDLIST_FILENAME = os.path.join(f"{__file__}", "..", "words.txt")


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    in_file = open(WORDLIST_FILENAME, "r")
    # wordList: list of strings
    word_list = []
    for line in in_file:
        word_list.append(line.strip().lower())
    print("  ", len(word_list), "words loaded.")
    return word_list


def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x, 0) + 1
    return freq


# (end of helper code)
# -----------------------------------


#
# Problem #1: Scoring a word
#


def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a valid word.

    The score for a word is the sum of the points for letters in the
    word, multiplied by the length of the word, PLUS 50 points if all n
    letters are used on the first turn.

    Letters are scored as in Scrabble; A is worth 1, B is worth 3, C is
    worth 3, D is worth 2, E is worth 1, and so on (see SCRABBLE_LETTER_VALUES)

    word: string (lowercase letters)
    n: integer (HAND_SIZE; i.e., hand size required for additional points)
    returns: int >= 0
    """
    score = 0
    for char in word:
        score += SCRABBLE_LETTER_VALUES[char] * len(word)
    if n == len(word):  # extra points for using all the letters
        score += 50

    return score


#
# Problem #2: Make sure you understand how this function works and what it does!
#
def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
    >>> display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """
    for letter in hand.keys():
        for j in range(hand[letter]):
            print(letter, end=" ")  # print all on the same line
    print()  # print an empty line


#
# Problem #2: Make sure you understand how this function works and what it does!
#
def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    At least n/3 the letters in the hand should be VOWELS.

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    hand = {}
    num_vowels = n // 3  # rounds the division to the nearest integer

    for i in range(num_vowels):
        x = VOWELS[random.randrange(0, len(VOWELS))]
        hand[x] = hand.get(x, 0) + 1

    for i in range(num_vowels, n):
        x = CONSONANTS[random.randrange(0, len(CONSONANTS))]
        hand[x] = hand.get(x, 0) + 1

    return hand


#
# Problem #2: Update a hand by removing letters
#
def update_hand(hand, word):
    """
    Assumes that 'hand' has all the letters in word.
    In other words, this assumes that however many times
    a letter appears in 'word', 'hand' has at least as
    many of that letter in it.

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)
    returns: dictionary (string -> int)
    """

    new_hand = dict(hand)  # copying the hand to form the updated hand

    for letter in word:
        new_hand[letter] = new_hand[letter] - 1

    return new_hand


#
# Problem #3: Test word validity
#
def is_valid_word(word, hand, word_list):
    """
    Returns True if word is in the wordList and is entirely
    composed of letters in the hand. Otherwise, returns False.

    Does not mutate hand or wordList.

    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    """
    # first condition: do we have enough letters in hand
    for letter in word:
        count = word.count(letter)
        if (
            hand.get(letter, 0) - count < 0
        ):  # hand.get returns the number of occurence of letter in word, if none it returns zero
            return False

    # second condition: does the word exist in the word list
    for item in word_list:
        if item == word:
            return True

    return False


#
# Problem #4: Playing a hand
#


def calculate_hand_length(hand):
    """
    Returns the length (number of letters) in the current hand.

    hand: dictionary (string-> int)
    returns: integer
    """

    hand_lenght = 0

    for letter in hand:
        hand_lenght += hand[letter]
    if hand_lenght == 0:
        print("No more letters to play")

    return hand_lenght


def play_hand(hand, word_list, n):
    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.
    * The user may input a word or a single period (the string ".")
      to indicate they're done playing
    * Invalid words are rejected, and a message is displayed asking
      the user to choose another word until they enter a valid word or "."
    * When a valid word is entered, it uses up letters from the hand.
    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.
    * The sum of the word scores is displayed when the hand finishes.
    * The hand finishes when there are no more unused letters or the user
      inputs a "."

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
      n: integer (HAND_SIZE; i.e., hand size required for additional points)

    """
    # BEGIN PSEUDOCODE <-- Remove this comment when you code this function; do your coding within the pseudocode (leaving those comments in-place!)
    # Keep track of the total score

    final_score = 0
    N = len(hand)

    for word in hand:

        # As long as there are still letters left in the hand:
        if n == 0:
            print("Run out of letters.")
            break

        else:
            print(f"You have {calculate_hand_length(hand)} letters left: ")

        # Display the hand

        display_hand(hand)

        # Ask user for input

        word = input('Enter word, or a "." to indicate that you are finished playing: ')

        # If the input is a single period:

        if word == ".":

            # End the game (break out of the loop)
            break

        # Otherwise (the input is not a single period):

        else:

            # If the word is not valid:

            if is_valid_word(word, hand, word_list) is False:

                # Reject invalid word (print a message followed by a blank line)
                print("Invalid word, please try again.")

            # Otherwise (the word is valid):

            else:

                # Tell the user how many points the word earned, and the updated total score, in one line followed by a blank line

                print(f"{word} earned {get_word_score(word, N)} points!")
                final_score += get_word_score(word, N)
                print(f"Total score: {final_score}")

                # Update the hand

                hand = update_hand(hand, word)
                n -= len(word)

    # Game is over (user entered a '.' or ran out of letters), so tell user the total score

    print(f"Game ended. Your total score is {final_score}", end="\n")


#
# Problem #5: Playing a game
#


def play_game(word_list, hand, play_count):
    """
    Allow the user to play an arbitrary number of hands.

    1) Asks the user to input 'n' or 'r' or 'e'.
      * If the user inputs 'n', let the user play a new (random) hand.
      * If the user inputs 'r', let the user play the last hand again.
      * If the user inputs 'e', exit the game.
      * If the user inputs anything else, tell them their input was invalid.

    2) When done playing the hand, repeat from step 1
    """

    answer = input(
        "Enter n to deal a new hand, r to replay the last hand, or e to end game:"
    )

    if answer == "n":
        hand = deal_hand(HAND_SIZE)
        play_hand(hand, word_list, HAND_SIZE)
        play_game(word_list, hand, play_count + 1)

    elif answer == "r":
        if play_count == 1:
            print("You have not played a hand yet. Please play a new hand first!")
            play_game(word_list, hand, play_count)
        else:
            play_hand(hand, word_list, HAND_SIZE)
            play_game(word_list, hand, play_count + 1)

    elif answer == "e":
        print("Game ended", end=" ")

        return False

    else:
        print("Invalid command.")


#
# Build data structures used for entire session and play game
#
if __name__ == "__main__":
    word_list = load_words()
    initial_hand = deal_hand(HAND_SIZE)
    play_count = 1
    play_game(word_list, initial_hand, play_count)
