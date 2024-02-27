import numpy as np
from numpy import random
from itertools import permutations
import json


class Sak:
    def __init__(self):
        self.randomize_sak()
        return

    def randomize_sak(self):
        self.dictionary = {'Α': [12, 1], 'Ε': [8, 1], 'Η': [7, 1], 'Ι': [8, 1], 'Ν': [6, 1], 'Ο': [9, 1], 'Σ': [7, 1], 'Τ': [8, 1], 'Κ': [4, 2], 'Π': [4, 2], 'Ρ': [5, 2], 'Υ': [
            4, 2], 'Λ': [3, 3], 'Ω': [3, 3], 'Μ': [3, 3], 'Γ': [2, 4], 'Δ': [2, 4], 'Β': [1, 8], 'Φ': [1, 8], 'Χ': [1, 8], 'Ζ': [1, 10], 'Θ': [1, 10], 'Ξ': [1, 10], 'Ψ': [1, 10]}
        self.sack = 102

    def getletters(self, letterlist, tobeadded):
        print("Mphka stin getletters :"+str(letterlist))
        alphabet = ['\u0391', '\u0392', '\u0393', '\u0394', '\u0395', '\u0396', '\u0397', '\u0398', '\u0399', '\u039A', '\u039B',
                    '\u039C', '\u039D', '\u039E', '\u039F', '\u03A0', '\u03A1', '\u03A3', '\u03A4', '\u03A5', '\u03A6', '\u03A7', '\u03A8', '\u03A9']
        # if there are k available letters
        if (tobeadded <= self.sack):
            for i in range(tobeadded):
                while True:
                    pot_letter = alphabet[random.randint(24)]
                    if (self.dictionary.get(pot_letter)[0] > 0):
                        letterlist.append(pot_letter)
                        self.dictionary.get(pot_letter)[0] -= 1
                        break
            self.sack -= tobeadded
            return self.dictionary, letterlist
        else:
            return {}, []

    def uniqueletters(self, list):
        unique_dict = {}
        for i in list:
            if i not in unique_dict.keys():
                unique_dict[i] = 1
            else:
                unique_dict[i] = unique_dict.get(i)+1
        return unique_dict

    def putbackletters(self, letter_list, keyword, p):
        # keyword=ZVH
        if (len(keyword) <= self.sack):
            if (p):
                for i in letter_list:
                    self.dictionary.get(i)[0] += 1
                letter_list = []
                dummy1, dummy2 = self.getletters(letter_list, 7)
                if (dummy1 == {} and dummy2 == []):
                    return False
                else:
                    self.dictionary, letter_list = dummy1, dummy2
                    self.sack += 7
                return letter_list
            else:
                char_list = list(keyword)
                for icounter, i in enumerate(char_list):
                    for jcounter, j in enumerate(letter_list):
                        if (i == j):
                            letter_list.pop(jcounter)
                            break
                dummy1, dummy2 = self.getletters(letter_list, len(char_list))
                if (dummy1 == {} and dummy2 == []):
                    return False
                else:
                    self.dictionary, letter_list = dummy1, dummy2
                return letter_list
        else:
            return False


class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.letters = []

    def __repr__(self) -> str:
        if (isinstance(self, Computer)):
            return (str(self.name)+" has "+str(self.score)+" points!")
        else:
            return (str(self.name)+", your points are "+str(self.score)+"!")


class Human(Player):

    def uniqueletters(self, list):
        unique_dict = {}
        for i in list:
            if i not in unique_dict.keys():
                unique_dict[i] = 1
            else:
                unique_dict[i] = unique_dict.get(i)+1
        return unique_dict

    def wordisok(self, keyword, letters):
        if (keyword == 'p'):
            return False
        if (len(keyword) > 1 and len(keyword) < 8):
            if keyword in file1:
                char_list = list(keyword)
                char_dict = self.uniqueletters(char_list)
                letter_dict = self.uniqueletters(letters)
                print(letter_dict)
                for letter in char_list:
                    # print(letter)
                    # print(letters)
                    if (letter not in letters):
                        # print("Το "+letter+" δεν υπάρχει στα γραμματά σου.")
                        return False
                    else:
                        if (letter_dict.get(letter) == 0):
                            # print('Δεν έχεις άλλα διαθέσιμα '+letter)
                            return False
                        else:
                            letter_dict[letter] = letter_dict.get(letter)-1
                return True
            else:
                return False
        else:
            print("Too small or too big")
            return False

    def calcscore(self, keyword, sak):
        char_list = list(keyword)
        mini_score = 0
        for i in char_list:
            mini_score += sak.dictionary.get(i)[1]
        print("Κέρδισες "+str(mini_score)+" πόντους!")
        self.score += mini_score

    def fillletters(self, sak):
        a, self.letters = sak.getletters([], 7)
        return

    def getword(self):
        word = input("Λέξη: ")
        while (self.wordisok(word, self.letters) == False and not (word == 'p' or word == 'q')):
            if word == 'p' or word == 'q':
                break
            else:
                word = input("Έδωσες λάθος λέξη, ξαναδώσε καινούρια: ")
        return word

    def decision(self, word, sak):
        if word == 'p':
            dummy = sak.putbackletters(self.letters, "", True)
            if (dummy == False):
                print("Δεν υπάρχει άλλη διαθέσιμη 7άδα γραμμάτων. Τέλος παιχνιδιού!")
                Game.end()
            else:
                self.letters = dummy
        elif word == 'q':
            self.end()
        else:
            self.calcscore(word, sak)
            dummy = sak.putbackletters(self.letters, word, False)
            if (dummy == False):
                print("Δεν υπάρχουν άλλα διαθέσιμα γράμματα. Τέλος παιχνιδιού!")
                Game.end()
            else:
                self.letters = dummy

    def play(self, sak):
        word = self.getword()
        self.decision(word, sak)


class Computer(Player):
    def __init__(self):
        self.name = "CPU"
        self.score = 0
        self.letters = []
        self.choise = "smart"

    def minletters(self, charset, words):
        for r in range(2, 7):
            for i in permutations(charset, r):
                if (''.join(i) in words):
                    return (''.join(i))
        return ""

    def maxletters(self, charset, words):
        for r in range(7, 2, -1):
            for i in permutations(charset, r):
                if (''.join(i) in words):
                    return (''.join(i))
        return ""

    def smart(self, charset, words, sak):
        acclist = []
        for r in range(2, 7):
            for i in permutations(charset, r):
                if (''.join(i) in words):
                    if (''.join(i) not in acclist):
                        acclist.append(''.join(i))
        max = -1
        maxword = ""
        for i in acclist:
            score = self.smartscore(i, sak)
            if (max < score):
                max = score
                maxword = i
        return maxword

    def calcscore(self, keyword, sak):
        char_list = list(keyword)
        for i in char_list:
            self.score += sak.dictionary.get(i)[1]

    def smartscore(self, keyword, sak):
        char_list = list(keyword)
        smartscore = 0
        for i in char_list:
            smartscore += sak.dictionary.get(i)[1]
        return smartscore

    def fillletters(self, sak):
        a, self.letters = sak.getletters([], 7)
        return

    def getword(self, sak):
        word = ''
        if self.choise == "max":
            word = self.maxletters(self.letters, file1)
        elif self.choise == "min":
            word = self.minletters(self.letters, file1)
        elif self.choise == "smart":
            word = self.smart(self.letters, file1, sak)
        return word

    def decision(self, word, sak):
        if (word != ""):
            print("Ο CPU επέλεξε την λέξη:" + word)
            self.calcscore(word, sak)
            dummy = sak.putbackletters(self.letters, word, False)
            if (dummy == False):
                print("Δεν υπάρχουν άλλα διαθέσιμα γράμματα. Τέλος παιχνιδιού!")
                Game.end()
            else:
                self.letters = dummy
        else:
            dummy = sak.putbackletters(self.letters, "", True)
            print("Ο CPU δεν βρήκε λέξη")
            if (dummy == False):
                print("Δεν υπάρχει άλλη διαθέσιμη 7άδα γραμμάτων. Τέλος παιχνιδιού!")
                Game.end()
            else:
                self.letters = dummy

    def play(self, sak):
        word = self.getword(sak)
        self.decision(word, sak)


class Game():
    def __init__(self, name):
        self.sak = Sak()
        self.player = Human(name)
        self.computer = Computer()
        self.rounds = 0
        return

    def __repr__():
        return

    def scoreboard(self):
        return

    def settings(self):
        algo = input(
            "Δίαλεξε αλγόριθμο για τον CPU \n 1. max \n 2. min \n 3. smart \n 4. back \n")
        while (not (algo == "1" or algo == "2" or algo == "3" or algo == "4")):
            print("Λάθος input! Ξαναδώσε επιλογή.")
            algo = input()
        if (algo == "1"):
            self.computer.choise = "max"
        elif (algo == "2"):
            self.computer.choise = "min"
        elif (algo == "3"):
            self.computer.choise = "smart"
        elif (algo == "4"):
            return
        return

    def setup(self):
        return

    def run(self):
        while True:
            if (self.rounds == 0):
                self.player.fillletters(self.sak)
            print("Το σακούλι έχει: "+str(self.sak.sack))
            print("Το σκόρ σου μέχρις στιγμής είναι: "+str(self.player.score))
            print("Τα γράμματα που έχεις διαθέσιμα για αυτόν τον γύρο είναι: " +
                  str(self.player.letters))
            self.player.play(self.sak)

            if (self.rounds == 0):
                self.computer.fillletters(self.sak)
            print("Το σακούλι έχει: "+str(self.sak.sack))
            print("Το σκόρ του CPU μέχρις στιγμής είναι: " +
                  str(self.computer.score))
            print("Τα γράμματα που έχει διαθέσιμα για αυτόν τον γύρο είναι: " +
                  str(self.computer.letters))
            self.computer.play(self.sak)
            self.rounds += 1

    def write_json(self, data):
        with open("scores.json", "w", encoding="utf8") as f:
            json.dump(data, f, indent=4)

    def end(self,decision):
        if (self.player.score > self.computer.score):
            print("Νίκησες, είχες "+str(self.player.score) +
                  " πόντους ενώ ο CPU είχε"+str(self.computer.score))
            won = "player"
        elif (self.player.score < self.computer.score):
            print("Έχασες, είχες "+str(self.player.score) +
                  " πόντους ενώ ο CPU είχε"+str(self.computer.score))
            won = "cpu"
        else:
            print("Ισοπαλία, είχες και εσύ και ο CPU " +
                  str(self.player.score)+" πόντους")
            won = "anyone"

        with open("scores.json", 'r+', encoding="utf8") as json_file:
            data = json.load(json_file)
            temp = data["games"]
            y = {"username": self.player.name, "userscore": self.player.score, "pcscore": self.computer.score,
                 "rounds": self.rounds, "whowon": won, "algo": self.computer.choise}
            temp.append(y)
            self.write_json(data)
        exit()


dicfile = open('greek7.txt', 'r', encoding="utf8")
file1 = dicfile.read()
file1 = file1.split()
onoma=input("Δώσε όνομα: ")
game=Game(onoma)