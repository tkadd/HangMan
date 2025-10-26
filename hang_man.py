from numpy import log2

class HangMan:

    def __init__(self, n):
        self.n = n
        self.word = ['_']*n
        self.guesses = list('abcdefghijklmnopqrstuvwxyz')
        self.guessed = set()
        self.last_guess = None

        self.dictionary = []
        with open('dictionary.txt') as file:
            for line in file:
                word = line[:-1]
                if len(word) == n:
                    self.dictionary.append(line[:-1])
                if len(word) > n:
                    break

    def filter(self, letter):
        new_dictionary = []
        for word in self.dictionary:
            if not letter in word: new_dictionary.append(word)
        if not new_dictionary:
            raise ValueError("No valid words left in the dictionary.")
        else:
            self.dictionary = new_dictionary

    def update(self, word=None):
        if word is None:
            self.filter(self.last_guess)
        else:
            new_dictionary = []
            for temp_word in self.dictionary:
                res = self.result(self.last_guess, temp_word)
                if res == word: new_dictionary.append(temp_word)
            self.word = list(word)
            if not new_dictionary:
                raise ValueError("No valid words left in the dictionary.")
            else:
                self.dictionary = new_dictionary
        
    def result(self, letter, target):
        result = ''
        for i, chr in enumerate(self.word):
            if chr != '_': result += chr
            else:
                if letter == target[i]: result += letter
                else: result += '_'
        return result

    def entropy(self):
        guess_entropy = {}
        n = len(self.dictionary)
        for letter in self.guesses:
            result_count = {}
            for target in self.dictionary:
                res = self.result(letter, target)
                if res in result_count: result_count[res] += 1
                else: result_count[res] = 1
            entropy = -sum((count/n)*log2(count/n) for count in result_count.values())
            guess_entropy[letter] = entropy
        return guess_entropy
  
    def guess(self):
        if not self.dictionary:
            raise ValueError("No valid words left in the dictionary.")
        elif len(self.dictionary) == 1:
            return self.dictionary.pop()
        else:
            guess_entropy = self.entropy()
            guess = max(guess_entropy, key=guess_entropy.get)

            self.guessed.add(guess)
            self.guesses.remove(guess)
            self.last_guess = guess
            return guess

if __name__ == '__main__':
    game = HangMan(15)
    print('phosphorescence' in game.dictionary)
