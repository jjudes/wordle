# Wordle

A version of wordle to run command line.

To play the default version, simply clone the repo and run:
```
python3 wordle.py
```

The secret word list, English words dictionary, length of secret word, or limit on number of guesses can be modified via CLI:

```bash
python3 wordle.py --words <path/to/words> 
                  --dictionary <path/to/dictionary> 
                  --length <secret word length> 
                  --max_guesses <limit on number of guesses>
```

Note that the `words` and `dictionary` files should be formatted as a new-line separated text file with one word on each line
