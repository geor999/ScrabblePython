import numpy as np
from numpy import random
from itertools import permutations
import json
from tkinter import *
from tkinter import ttk
from waiting import wait
import time


class Sak:
    def __init__(self):
        self.randomize_sak()
        return
    #create the sak
    def randomize_sak(self):
        #'letter':[available from that letter,points]
        self.dictionary = {'Α': [12, 1], 'Ε': [8, 1], 'Η': [7, 1], 'Ι': [8, 1], 'Ν': [6, 1], 'Ο': [9, 1], 'Σ': [7, 1], 'Τ': [8, 1], 'Κ': [4, 2], 'Π': [4, 2], 'Ρ': [5, 2], 'Υ': [
            4, 2], 'Λ': [3, 3], 'Ω': [3, 3], 'Μ': [3, 3], 'Γ': [2, 4], 'Δ': [2, 4], 'Β': [1, 8], 'Φ': [1, 8], 'Χ': [1, 8], 'Ζ': [1, 10], 'Θ': [1, 10], 'Ξ': [1, 10], 'Ψ': [1, 10]}
        self.sack=102
    
    def getletters(self,letterlist,tobeadded):
        #alphabet create
        alphabet = ['\u0391', '\u0392', '\u0393', '\u0394', '\u0395', '\u0396', '\u0397', '\u0398', '\u0399', '\u039A', '\u039B',
                    '\u039C', '\u039D', '\u039E', '\u039F', '\u03A0', '\u03A1', '\u03A3', '\u03A4', '\u03A5', '\u03A6', '\u03A7', '\u03A8', '\u03A9']
        #if there are k available letters
        if(tobeadded<=self.sack):
            #for k letters
            for i in range(tobeadded):
                #True until it finds a letter that is available
                while True:
                    #random letter
                    pot_letter = alphabet[random.randint(24)]
                    #if this letter is available
                    if (self.dictionary.get(pot_letter)[0] > 0):
                        #append it to the list
                        letterlist.append(pot_letter)
                        #reduce its counter
                        self.dictionary.get(pot_letter)[0] -= 1
                        #break the loop for the next letter to be added
                        break
            #reduce sack letters number
            self.sack-=tobeadded
            return self.dictionary, letterlist
        else:
            #if not return empty
            return {},[]

    #find the unique letters from a a list and return them in a dictionary which has as key a letter and as value a counter of how many times the letter is in the list
    def uniqueletters(self, list):
        unique_dict = {}
        for i in list:
            if i not in unique_dict.keys():
                unique_dict[i] = 1
            else:
                unique_dict[i] = unique_dict.get(i)+1
        return unique_dict

    #function to put the letters back to the sack and refill the letter_list of the player or CPU
    def putbackletters(self, letter_list, keyword,p):
        #if there are k letters available
        if(len(keyword)<=self.sack):
            #if p is True(pass)
            if(p):
                #return the letters from the letter list
                for i in letter_list:
                    self.dictionary.get(i)[0] += 1
                #empty the letterlist
                letter_list = []
                #refill it with 7 letters or what's left
                #variable to keep how many letters we put back
                refilled=0
                if(self.sack>=7):
                    refilled=7
                    dummy1,dummy2=self.getletters(letter_list,7)
                else:
                    refilled=self.sack
                    dummy1,dummy2=self.getletters(letter_list,self.sack)
                #if there aren't enough letters to be refilled
                if(dummy1=={} and dummy2==[]):
                    return False
                else:
                    self.dictionary, letter_list = dummy1,dummy2
                    self.sack+=refilled
                return letter_list
            else:
                #separate the keyword
                char_list = list(keyword)
                #for each letter in keyword
                for icounter,i in enumerate(char_list):
                    #for each letter in letters
                    for jcounter,j in enumerate(letter_list):
                        #if they match
                        if(i==j):
                            #pop the letter from the keyword letter_list
                            letter_list.pop(jcounter)
                            break
                #call getletters
                dummy1,dummy2=self.getletters(letter_list,len(char_list))
                if(dummy1=={} and dummy2==[]):
                    return False
                else:   
                    self.dictionary, letter_list = dummy1,dummy2
                return letter_list
        else:
            return False

    def set_sak(self,value):
        self.dictionary=value
        
    def get_sak(self):
        return self.dictionary
class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.letters = []
        self.lastscore=0

    def __repr__(self) -> str:
        if (isinstance(self, Computer)):
            return (str(self.name)+" has "+str(self.score)+" points!")
        else:
            return (str(self.name)+", your points are "+str(self.score)+"!")
    
    def set_name(self,value):
        self.name=value

    def get_name(self):
        return self.name
    
    def set_score(self,value):
        self.score=value

    def get_score(self):
        return self.score
    
    def set_lastscore(self,value):
        self.lastscore=value

    def get_lastscore(self):
        return self.lastscore
    
    def set_letters(self,value):
        self.letters=value

    def get_letters(self):
        return self.letters
    
class Human(Player):
    #find the unique letters from a a list and return them in a dictionary which has as key a letter and as value a counter of how many times the letter is in the list
    def uniqueletters(self, list):
        unique_dict = {}
        for i in list:
            if i not in unique_dict.keys():
                unique_dict[i] = 1
            else:
                unique_dict[i] = unique_dict.get(i)+1
        return unique_dict

    #function that checks if the word is ok based on the letter_list
    def wordisok(self, keyword, letters):
        if(keyword=='p'):
            return False
        elif(keyword=='q'):
            return False
        #check size
        elif( len(keyword)>1 and len(keyword)<8):
            #if keyword exists
            filelist=fileinit()
            if keyword in filelist:
                #separate
                char_list = list(keyword)
                #find unique letters
                char_dict = self.uniqueletters(char_list)
                letter_dict = self.uniqueletters(letters)
                #for each letter in keyword check if it can be actually used
                for letter in char_list:
                    # print(letter)
                    # print(letters)
                    #if it isn't on available letters
                    if (letter not in letters):
                        # print("Το "+letter+" δεν υπάρχει στα γραμματά σου.")
                        return False
                    else:
                        #if the counter of this letter is 0 it means we have no more of it left 
                        if (letter_dict.get(letter) == 0):
                            # print('Δεν έχεις άλλα διαθέσιμα '+letter)
                            return False
                        else:
                            #reduce the counter of the letter
                            letter_dict[letter] = letter_dict.get(letter)-1
                #if everything is ok return true
                return True
            else:
            #if keyword doesnt exist return False
                return False
        else:
            #if keyword size isn't between 2 and 7 return false
            return False
    
    #function that calculates player's score after the player finds a new word     
    def calcscore(self,keyword,sak):
        #calculate the keywords score
        keyword_score=self.wordscore(keyword,sak)
        #add the score to the CPU score
        self.score+=keyword_score
        #return the keyword's points for UI purpose
        return keyword_score

    def wordscore(self,keyword,sak):
        #separate the keyword
        char_list = list(keyword)
        dummy=0
        #for each letter
        for i in char_list:
            #add the points
            dummy+=sak.dictionary.get(i)[1]
        #return the keyword's points for UI purpose
        return dummy

    #function that fills the letter_list of the computer. It's called only the first round    
    def fillletters(self,sak):
        a, self.letters = sak.getletters([],7)
        return
    
    #function that if the player found a word calculates the score of it and refills the letter_list, else if word="p" checks if there are any letters to replace the letterlist else if word="q" end game
    def decision(self,word,sak):
        #check word
        if word=='p':
            #check if there are available k letters to replace
            dummy=sak.putbackletters(self.letters,"",True)
            #if not end game
            if(dummy==False):
                return "Δεν υπάρχει άλλη διαθέσιμη 7άδα γραμμάτων. Τέλος παιχνιδιού!"
            else:
                #replace letters
                self.letters=dummy
                self.lastscore=0
                return 0
        elif word=='q':
            #end game
            return "Το παιχνίδι τελείωσε!"
        else:   
            #set lastscore to the word's score
            self.lastscore=self.calcscore(word,sak)
            #check if can be refilled
            dummy=sak.putbackletters(self.letters,word,False)
            if(dummy==False):
                #if not end game
                return "Δεν υπάρχουν άλλα διαθέσιμα γράμματα. Τέλος παιχνιδιού!"
            else:
                #refill
                self.letters=dummy
                return 0
                

    def play(self,word,sak):
        decision=self.decision(word,sak)
        return decision
        
    def get_letters(self):
        return self.letters


class Computer(Player):
    def __init__(self):
        self.name = "CPU"
        self.score = 0
        self.letters=[]
        self.algorithm="smartfail"
        self.lastscore=0


    def set_algorithm(self,value):
        self.algorithm=value
    def set_name(self,value):
        self.name=value
    def set_score(self,value):
        self.score=value
    def set_letters(self,value):
        self.letters=value
    def set_lastscore(self,value):
        self.lastscore=value
    
    def get_algorithm(self):
        return self.algorithm
    def get_name(self):
        return self.name
    def get_score(self):
        return self.score
    def get_letters(self):
        return self.letters
    def get_lastscore(self):
        return self.lastscore


    #function that gets the word with the least letters that can be created from the letter_list
    def minletters(self,charset,words):
        for r in range(2,7):
            for i in permutations(charset,r):
                if(''.join(i) in words):
                    return(''.join(i))
        return ""
    
    #function that gets the word with the most letters that can be created from the letter_list     
    def maxletters(self,charset,words):
        for r in range(7,2,-1):
            for i in permutations(charset,r):
                if(''.join(i) in words):
                    return(''.join(i))
        return ""
    
    #function that gets the word with the best score that can be created from the letter_list        
    def smart(self,charset,words,sak):
        acclist=[]
        for r in range(2,7):
            for i in permutations(charset,r):
                if(''.join(i) in words):
                    if (''.join(i) not in acclist):
                        acclist.append(''.join(i))
        max=-1
        maxword=""
        for i in acclist:
            score=self.wordscore(i,sak)
            if(max<score):
                max=score
                maxword=i
        return maxword

    #probablistic function that based on a random number returns a different word from the words found each round and not only the one with the best score        
    def smart_fail(self,charset,words,sak):
        acclist=[]
        for r in range(2,7):
            for i in permutations(charset,r):
                if(''.join(i) in words):
                    if (''.join(i) not in acclist):
                        acclist.append(''.join(i))
        scores=[]
        for i in acclist:
            scores.append(self.wordscore(i,sak))
        acclist,scores=[x for y, x in sorted(zip(scores, acclist))],[y for y, x in sorted(zip(scores, acclist))]
        random_num=np.random.rand()
        #if AI found 3 or more words and 0.7>random_num>0.6 return word with third best score else if 0.7<random_num return second best and if 0.5>random_num return best word
        if(len(acclist)>2):
            if(random_num>0.6 and random_num<0.7):
                return acclist[len(acclist)-3]
            if(random_num>0.7):
                return acclist[len(acclist)-2]
            return acclist[len(acclist)-1]
        #if AI found 2 or more words and 0.6<random_num return word with second best score else if 0.6>random_num return best word
        elif(len(acclist)==2):
            if(random_num>0.6):
                return acclist[len(acclist)-2]
            return acclist[len(acclist)-1]
        #if AI found 1 word and 0.1<random_num return the word else if 0.1>random_num return empty string so it has a chance to not find the word
        elif(len(acclist)==1):
            if(random_num>0.1):
                return acclist[len(acclist)-1]
            return ""
        #if AI didn't find any words returns empty string
        elif(len(acclist)==0):return ""

    #function that calculates CPU's score after CPU finds a new word
    def calcscore(self,keyword,sak):
        #calculate the keywords score
        keyword_score=self.wordscore(keyword,sak)
        #add the score to the CPU score
        self.score+=keyword_score
        #return the keyword's points for UI purpose
        self.lastscore=keyword_score
    
    def wordscore(self,keyword,sak):
        #separate the keyword
        char_list = list(keyword)
        dummy=0
        #for each letter
        for i in char_list:
            #add the points
            dummy+=sak.dictionary.get(i)[1]
        #return the keyword's points for UI purpose
        return dummy

    #function that fills the letter_list of the computer. It's called only the first round
    def fillletters(self,sak):
        a, self.letters = sak.getletters([],7)
        return
    
    #function that based on the algorithm we use calls the respective function
    def getword(self,sak):
        word=''
        filelist=fileinit()
        if self.algorithm=="max":
            word=self.maxletters(self.letters,filelist)
        elif self.algorithm=="min":
            word=self.minletters(self.letters,filelist)
        elif self.algorithm=="smart":
            word=self.smart(self.letters,filelist,sak)
        elif self.algorithm=="smartfail":
            word=self.smart_fail(self.letters,filelist,sak)
        return word
    
    #function that if the CPU found a word calculates the score if there is a word and refills the letter_list, else if it didn't find any words checks if there are any letters to refill
    def decision(self,word,sak):
        #check word
        if(word!=""):
            #if word is not empty string
            #calculate score
            self.calcscore(word,sak)
            #put k letters back if there are available
            dummy=sak.putbackletters(self.letters,word,False)
            #if there weren't any available end the game
            if(dummy==False):
                return "Δεν υπάρχουν άλλα διαθέσιμα γράμματα. Τέλος παιχνιδιού!"
            else:
                #else refill the letters
                self.letters=dummy
                #return the score of the word
                return 0
        else:
            #if word is empty string
            #check if there are available letters to replace the whole letter_list
            dummy=sak.putbackletters(self.letters,"",True)
            #if not end game
            if(dummy==False):
                return "Ο CPU δεν βρήκε λέξη. Δεν υπάρχει άλλη διαθέσιμη 7άδα γραμμάτων. Τέλος παιχνιδιού!"
            else:
                #else replace
                self.letters=dummy
                return 0
    #function that plays the round for CPU
    def play(self,sak):
        #get the word
        word=self.getword(sak)
        #check that word and get the score for it
        return self.decision(word,sak)
        
class Game():
    def __init__(self,name):
        self.sak = Sak()
        self.player = Human(name)
        self.computer = Computer()
        self.rounds=0
        self.ended=False
        self.end_reason=""
        return
    
    def __repr__():
        return
    
    def scoreboard(self):
        return
    
    
    def setup(self):
        self.player.fillletters(self.get_sack())
        self.computer.fillletters(self.get_sack())
        return
    
    def set_algo(self,value):
        self.computer.set_algorithm(value)

    def player_set_name(self,value):
        self.player.set_player(value)

    def set_rounds(self,value):
        self.rounds=value

    def get_player(self):
        return self.player
    
    def get_computer(self):
        return self.computer
    
    def get_ended(self):
        return self.ended

    def get_end_reason(self):
        return self.end_reason
    
    def get_sack(self):
        return self.sak

    def get_algo(self):
        return self.computer.get_algorithm()
    
    
    
    
    def run(self,turn):
        if(turn%2==0):
            return self.player.play(self.sak)
        else:
            return self.computer.play(self.sak)
            

    def write_json(self,data):
        with open("scores.json","w",encoding="utf8") as f:
            json.dump(data,f,indent=4)
     
    def end(self,reason):
        if(self.player.score>self.computer.score):
            result="Νίκησες, είχες "+str(self.player.get_score())+" πόντους ενώ ο CPU είχε "+str(self.computer.get_score())+"!"
            won="player"
        elif(self.player.score<self.computer.score):
            result="Έχασες, είχες "+str(self.player.get_score())+" πόντους ενώ ο CPU είχε "+str(self.computer.get_score())+"!"
            won="cpu"
        else:
            result="Ισοπαλία, είχες και εσύ και ο CPU "+str(self.player.get_score())+" πόντους!"
            won="anyone"

        with open("scores.json",'r+',encoding="utf8") as json_file:
            data=json.load(json_file)
            temp=data["games"]
            y={"username": self.player.get_name(), "userscore": self.player.get_score(),"pcscore": self.computer.get_score(),"rounds":self.rounds,"whowon":won,"algo":self.computer.get_algorithm()}
            temp.append(y)
            self.write_json(data)
        self.ended=True
        self.end_reason=reason
        return result

def fileinit():
    dicfile = open('greek7.txt', 'r', encoding="utf8")
    file1 = dicfile.read()
    file1 = file1.split()
    return file1