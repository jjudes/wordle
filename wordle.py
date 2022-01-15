import re
import argparse
import random
from functools import wraps
from time import time


def timer(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time()
        result = f(*args, **kw)
        elapsed = time() - ts
        if elapsed < 60:
            print(f"Time Elapsed: {elapsed} seconds")
        else:
            print(f"Time Elapsed: {elapsed / 60} minutes")
        return result
    return wrap


class Display:
    
    # Colour Codes
    COLOURS = {
        'pink': '\033[95m',
        'blue': '\033[94m',
        'cyan': '\033[96m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'red': '\033[91m'
    }
    
    # Formatting Codes
    BOLD = '\033[1m'
    UNDERLINE ='\033[4m'
    END = '\033[0m'
    
    @classmethod
    def format(cls, text, colour=None, bold=False, underline=False):
        
        if not any([colour, bold, underline]):
            return text
        
        header = ''
        footer = Display.END
                
        if bold:
            header += Display.BOLD
        if underline:
            header += Display.UNDERLINE
        if colour:
            header += Display.COLOURS[colour]
        
        return f"{header}{text}{footer}"


class Wordle:
    
    def __init__(self, words, dictionary, length=5, max_guesses=6):
        
        # Check that word length and number of guesses inputs are valid
        assert length >= 2 and max_guesses >= 2
        self.length = int(length)
        self.max_guesses = int(max_guesses)

        # Filter words to the specified length, in case it's not already
        words = set(w for w in words if len(w) == self.length)
        assert len(words) > 0
        self.words = words
        
        self.dictionary = set(w for w in dictionary if len(w) == self.length).union(words)
        
        # Stopping command
        self.stop = "!"
    
    @timer
    def game(self):
        
        self.intro()
        
        target = random.sample(self.words, 1)[0]
        
        empty = " " * self.length
        print(self.grid(empty, empty))
        
        guesses = 0
        solved = False
        previous = None
        
        while guesses < self.max_guesses:
            
            guess = input("Enter your guess: ")
            if guess == self.stop:
                break
        
            # Scrub superfluous whitespace
            guess = re.sub(r'\s+', '', guess)
            
            # Check input validity
            is_valid = self.check_input(guess, previous, target)
            if not is_valid:
                continue
            
            guesses += 1
            print(self.grid(guess, target))
            previous = guess
            
            if guess == target:
                solved = True
                break
        
        if solved:
            print(f"Congratulations! You correctly guessed the secret word {Display.format(target, 'green', bold=True)} with {guesses} guesses!")
        elif guesses < self.max_guesses:
            print(f"Thanks for playing! The secret word was {Display.format(target, 'green', bold=True)}.")
        else:
            print(f"Good Try! The secret word was {Display.format(target, 'green', bold=True)}.")
    
    def check_input(self, guess, previous, target):
        
        if not re.match(r'^[A-Za-z]+$', guess):
            print("Guess contains non-alphabetic letters or special characters. Try again!\n")
            return False

        if len(guess) != self.length:
            print(f"Your guess must be a {self.length} letter word. Try again!\n")
            return False
        
        if guess not in self.dictionary:
            print("We don't think this is a valid English word. Try again!\n")
            return False
        
        if previous:
            if previous == guess:
                print("Guess matches your previous guess. Try something new!\n")
                return False
            target_set = set(target)
            misplaced = set(p for p, t in zip(previous, target) if p != t and p in target_set)
            for i in range(self.length):
                if previous[i] == target[i] and guess[i] != previous[i]:
                    print("Correctly guessed letters cannot be changed. Try again!\n")
                    return False
                misplaced.discard(guess[i])
            if len(misplaced) > 0:
                print("Out-of-place letters must be used in your new guess. Try again!\n")
                return False

        return True
    
    def intro(self):
        
        print(Display.format("Welcome to Jef's bootleg Wordle!", colour="blue", bold=True))
        print('-'*40)
        print(f"\nThe goal of the game is to guess a secret {self.length} letter word (with no hyphens or special characters).\n\n" \
            f"In each round you will be able to guess any {self.length} letter word.\n\n" \
            f"If a letter in your guess is in the right place, it will be displayed {Display.format('green', 'green', bold=True)}\n\n" \
            f"{self.grid('A--', 'A++')}\n\n" \
            f"If a letter in your guess is in the word but in the wrong place, it will be displayed {Display.format('yellow', 'yellow', bold=True)}\n\n" \
            f"{self.grid('-A-', 'A++')}\n\n" \
            f"In your next guess, you'll have to keep those {Display.format('correct', 'green', bold=True)} letters in place and use the " \
            f"{Display.format('out-of-place', 'yellow', bold=True)} letters somewhere else.\n" \
            f"You will get a maximum of {self.max_guesses} guesses to find the secret word.\n\n" \
            f"Enter {self.stop} at any time to exit.\n\n" \
            "Good luck!\n""")
        print('-'*40 + '\n')
    
    @classmethod
    def grid(cls, guess, target):
        
        length = len(target)
        assert len(guess) == len(target)
        
        boundary = '+---' * length + '+'
        row = ''
        for g, t in zip(guess, target):
            
            if g == t:
                letter = Display.format(g, colour='green', bold=True)
            elif g in target:
                letter = Display.format(g, colour='yellow', bold=True)
            else:
                letter = Display.format(g, bold=True)
            
            row += f'| {letter} '
        row += '|'
        return f'{boundary}\n{row}\n{boundary}'


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--length', type=int, help='Length of word to guess', default=5)
    parser.add_argument('--max_guesses', type=int, help='Maximum number of guesses', default=6)
    parser.add_argument('--words', help='List of secret words for games', default='./words.txt')
    parser.add_argument('--dictionary', help='List of valid English words for guesses', default='./dictionary.txt')
    
    args = parser.parse_args()
    
    with open(args.words) as f:
        words = set(f.read().split())

    with open(args.dictionary) as f:
        dictionary = set(f.read().split())

    wordle = Wordle(words, dictionary, args.length, args.max_guesses)
    wordle.game()
