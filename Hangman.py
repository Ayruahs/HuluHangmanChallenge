"""
The logic of my code is as follows: I first check for the most frequent letters in the hangman phrase.
After there is only one guess left, I use regular expressions to check for specific words from the 
list of most used words provided by Google, which is recorded in the "count_1w.txt" text files.
"""
import json
import requests
import time
import re

from MostCommonWords import wordSet

winCount = 0
lossCount = 0

url = "http://gallows.hulu.com/play?code=sinha35@purdue.edu"


while True:    

    resp = requests.get(url=url)
    data = resp.json()
    print("Welcome to a new game of hangman!")

    alive = 'ALIVE'
    dead = 'DEAD'
    free = 'FREE'

    phrase = data['state']
    TOKEN = data['token']
    status = data['status']
    guessesLeft = data['remaining_guesses']

    letters = list("etaoinsrhldcumfpgwybvkxjqz")

    guessedLetters = set()

    for letter in letters:
        if guessesLeft <2:
            break
        GUESS = letter
        guessedLetters.add(letter)
        gameUrl = "http://gallows.hulu.com/play?code=sinha35@purdue.edu&token=" + TOKEN + "&guess=" + GUESS
        resp1 = requests.get(url=gameUrl)
        data1 = resp1.json()

        phrase = data1['state']

        status = data1['status']
        guessesLeft = data1['remaining_guesses']




    while status == alive:


        words = phrase.split()
        wordsThatMatch = set()
        
        for word in words:
            if guessesLeft == 0:
                break
            indices = []
            k = 0
            if word.count('_') != 0:   
                regex = "^"
                for letter in word:
                    if letter == "_":
                        indices.append(k)
                        regex += "[a-zA-Z]"
                    else:
                        regex += letter.lower()
                    k += 1
                regex += "$"
            
            if word.count('_') != 0: 
                for i in wordSet:
                    match = re.match(regex, i)
                    if match:
                        wordsThatMatch.add(match.string)

            for w in wordsThatMatch:
                #if w not in guessedWords:
                #   guessedWords.add(w)
                for i in range(len(w)):
                    if i in indices:
                        GUESS = w[i]
                        if guessesLeft == 0:
                            break

                        gameUrl = "http://gallows.hulu.com/play?code=sinha35@purdue.edu&token=" + TOKEN + "&guess=" + GUESS
                        resp1 = requests.get(url=gameUrl)
                        data1 = resp1.json()

                        phrase = data1['state']

                        status = data1['status']
                        guessesLeft = data1['remaining_guesses']     




    if status == dead:
        lossCount += 1
    if status == free:
        winCount += 1


    print("The game is over!")
    print("You have won: %d times\nand lost: %d times." %(winCount, lossCount))
    print("Win Percentage is: %.4f%%" %(winCount / (winCount + lossCount) * 100))
    print("The total number of games played is: %d\n\n\n" %(winCount + lossCount))
