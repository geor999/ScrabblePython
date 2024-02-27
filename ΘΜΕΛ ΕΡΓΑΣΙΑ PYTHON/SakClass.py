from tkinter import *
from tkinter import ttk
import player2
from player2 import *


def guidelines():
    """
    Scrabble Game

    Αυτό το πρόγραμμα υλοποιεί ένα παιχνίδι Scrabble χρησιμοποιώντας την ελληνική γλώσσα.
    Επιτρέπει στους παίκτες να σχηματίσουν έγκυρες ελληνικές λέξεις χρησιμοποιώντας τα διαθέσιμα γράμματα.
    Το παιχνίδι συνεχίζεται μέχρι να αδειάσει ο σάκος ή ένας από τους παίκτες να μην μπορεί να σχηματίσει λέξη.
    Ο παίκτης με το υψηλότερο σκορ στο τέλος κερδίζει το παιχνίδι.

    Classes:
     - Game: Represents the game and its logic.
     - Player: Represents a player in the game.
     - ComputerPlayer: Represents a computer-controlled player.


    Inheritance:

    - Η Game κλάση χρησιμεύει ως βασική κλάση, ενώ η Player και η ComputerPlayer είναι κλάσεις που κληρονομούν από το παιχνίδι.


    Method Extensions:

    - Οι παραγόμενες κλάσεις (Player and ComputerPlayer) να εφαρμόσουν πρόσθετες μεθόδους που επεκτείνουν τη λειτουργικότητα της βασικής κλάσης.


    Operator Overloading / Decorators:

    - Υπερφόρτωση χειριστή ή διακοσμητές δεν χρησιμοποιούνται στον κώδικα.

    Word Organization:

    - Η εφαρμογή οργανώνει λέξεις σε μια δομή λεξικού, με τις λέξεις ως κλειδιά και τις ιδιότητες τους (e.g., score, length) ως τιμές.


    Algorithm:

    - Το παιχνίδι χρησιμοποιεί διάφορους αλγόριθμους για διαφορετικές λειτουργίες, όπως π.χ word validation, scoring, and computer player strategy.


    Usage:
    - Για να ξεκινήσετε το παιχνίδι, δημιουργήστε ένα στιγμιότυπο της κλάσης Game και καλέστε τη μέθοδο play_game().
    - Κατά τη διάρκεια του παιχνιδιού, οι παίκτες εισάγουν εναλλάξ λέξεις με βάση συγκεκριμένους κανόνες.
    - Η συσκευή αναπαραγωγής υπολογιστή χρησιμοποιεί αλγόριθμους για τη δημιουργία έξυπνων επιλογών λέξεων.
    - Το παιχνίδι συνεχίζεται έως ότου οι παίκτες αποφασίσουν να το τερματίσουν.

    
    Credits:
    - Developed by [Your Name]
    - Game engine: Scrabble
    - UI framework: Tkinter
    - Dictionary: Greek7
    """

# Function to show the UI of the help page
def helpmenu():
    hide_menu()
    help_text = """Welcome to Scrabble Help!

- In the game, you need to enter valid words using the available letters.
- The word should either be a valid Greek word or a two-letter word 'p' or 'q'.
- You can enter a word by typing it in the entry box and clicking OK.
- The computer will take its turn after you.
- The game continues until the sack is empty or one of the players cannot form a word.
- The player with the highest score wins the game.

Enjoy playing Scrabble!

Credits:
- Developed by [Your Name]
- Game engine: Scrabble
- UI framework: Tkinter
- Dictionary: Greek7"""

    help_label = Label(frame, text=help_text, font=('Arial', 12), justify=LEFT)
    help_label.pack(pady=(15, 0))

    back = ttk.Button(frame, text="Back", command=show_menu)
    back.pack(pady=(15, 0))


#function to show the UI of the main menu
def show_menu():
    for widgets in frame.winfo_children():
        if widgets != ".!frame.gamebutton" or widgets != ".!frame.scoreboardbutton" or widgets != ".!frame.settingsbutton" or widgets != ".!frame.helpbutton" or widgets != ".!frame.closebutton" or widgets != ".!frame.header":
            widgets.pack_forget()

    header.pack(pady=(15,0))
    game.pack(pady=(15, 0))
    settings.pack(pady=(15, 0))
    help_button.pack(pady=(15, 0))
    close.pack(pady=(15, 0))
    scoreboardmenu()

#function to hide the UI of the main menu
def hide_menu():
    header.pack_forget()
    game.pack_forget()
    scoreboard_label.pack_forget()
    scoreboard.pack_forget()
    settings.pack_forget()
    close.pack_forget()

#function to get the name of the player
def get_value():
    
    e_text=w.get()
    if(e_text!=""):
        global name_var
        name_var=e_text
        header.config(text="Καλωσόρισες "+e_text+"!")
        global gameclass
        gameclass=Game(name_var)
        show_menu()
    else:
        error.pack()


def waithere():
        
        var.set(not var)

#callback function that gets the input from the entry
def get_word_callback():
        e_text=entry.get()
        #check if the word is ok so it can go on
        if(gameclass.player.wordisok(e_text, gameclass.player.get_letters()) or (e_text=='p' or e_text=='q')):
            global keyword_input
            keyword_input=e_text
            #set var True to unblock the program
            var.set(True)
        else:
            error.pack()

def getword():
        #create ui
        title=Label(frame,text="Πληκτρολογήστε μια λέξη!")
        title.pack()
        error.config(text="Η λέξη ήταν λάθος ξαναπροσπάθησε!",fg="red")
        entry.pack(pady= 30)
        #button with callback the get_word_callback which gets the input
        button= ttk.Button(frame, text="ΟΚ!", command= get_word_callback)
        button.pack()
        #wait for var to be set to True so it can go on running the code
        screen.wait_variable(var)
        #when the var is set to true the UI goes away for the results to be shown
        title.pack_forget()
        entry.pack_forget()
        button.pack_forget()
        error.pack_forget()
        #clear the entry
        entry.delete(0, END)

def startgame():
    gameclass.setup()
    hide_menu()
    t=0
    while(gameclass.ended==False):
        if(t%2==0):
            label.config(text="Το σακούλι έχει: "+str(gameclass.sak.sack)+"\n Το σκόρ σου μέχρις στιγμής είναι: "+str(gameclass.player.score)+"\n Τα γράμματα που έχεις διαθέσιμα για αυτόν τον γύρο είναι: "+str(gameclass.player.letters) ,font= ('Arial'))
            label.pack()
            getword()
            decision=gameclass.player.play(keyword_input,gameclass.get_sack())
            if(decision==0):
                if(gameclass.player.lastscore==None):
                        gameclass.player.lastscore=0
                label.config(text="Το σακούλι έχει: "+str(gameclass.sak.sack)+"\n Το σκόρ σου μέχρις στιγμής είναι: "+str(gameclass.player.score)+"\n Κέρδισε "+str(gameclass.player.lastscore)+" πόντους! \n Δίαλεξες την λέξη "+keyword_input ,font= ('Arial'))
                screen.after(2000, waithere)
                screen.wait_variable(var)
                t=t+1
            else:
                result=gameclass.end(decision)
                endscreen(result)
        else:
            label.pack_forget()
            label.config(text="Το σακούλι έχει: "+str(gameclass.sak.sack)+"\n Το σκόρ του CPU μέχρις στιγμής είναι: "+str(gameclass.computer.score)+"\n Τα γράμματα που έχει διαθέσιμα για αυτόν τον γύρο είναι: "+str(gameclass.computer.letters) ,font= ('Arial'))
            label.pack()
            screen.after(2000, waithere)
            screen.wait_variable(var)
            decision=gameclass.run(t)
            if(decision==0):
                if(gameclass.computer.lastscore==None):
                    gameclass.computer.lastscore=0
                label.config(text="Το σακούλι έχει: "+str(gameclass.sak.sack)+"\n Το σκόρ του CPU μέχρις στιγμής είναι: "+str(gameclass.computer.score)+"\n Κέρδισε "+str(gameclass.computer.lastscore)+" πόντους!" ,font= ('Arial'))
                screen.after(2000, waithere)
                screen.wait_variable(var)
                t=t+1
            else:
                result=gameclass.end(decision)
                endscreen(result)
        if(t%2==0):
            gameclass.rounds+=1

def endscreen(result):
    end_reason=Label(frame,name='endreason',text=gameclass.get_end_reason())
    end_title=Label(frame,name='endtitle',text=result)
    for widgets in frame.winfo_children():
        if(widgets!=".!frame.endtitle" or widgets!=".!frame.endreason"):
            widgets.pack_forget()
    end_reason.pack(pady= 30)
    end_title.pack()

def endgame():
    exit()     


def scoreboardmenu():
    scoreboard_label.pack(pady=(15,0))
    scoreboard.pack(pady=(15,0))


#function for the UI of settings page
def settingsmenu():
    hide_menu()
    algo_label=Label(frame,text="Διαλέξτε αλγόριθμο για τον CPU!")
    algo_label.pack(pady=(10,0))
    min= ttk.Button(frame, text="Min",command=lambda *args: gameclass.set_algo("min"))
    min.pack(pady=(15,0))
    max= ttk.Button(frame, text="Max",command=lambda *args: gameclass.set_algo("max"))        
    max.pack(pady=(15,0))
    smart= ttk.Button(frame, text="Smart",command=lambda *args: gameclass.set_algo("smart"))       
    smart.pack(pady=(15,0))
    smartfail= ttk.Button(frame, text="Smart-Fail",command=lambda *args: gameclass.set_algo("smartfail"))       
    smartfail.pack(pady=(15,0))
    back= ttk.Button(frame, text="Back",command=show_menu)
    back.pack(pady=(15,0))

def fileinit():
    dicfile = open('greek7.txt', 'r', encoding="utf8")
    file1 = dicfile.read()
    file1 = file1.split()
    return file1


total_rows=None
total_columns=None
keyword_input=""
gameclass=None
name_var=None
filelist=fileinit()
screen=Tk()
screen.title("Scrabble")
screen.geometry("800x800")
frame = Frame(screen)
frame.pack(side="top", expand=True, fill="both")

#scores
with open("scores.json",'r+',encoding="utf8") as json_file:
            data=json.load(json_file)
            temp=data["games"]
            listed=[tuple(d.values()) for d in temp]
            scoreboard = ttk.Treeview(frame)

            scoreboard_label=Label(frame,name="scoreboard_label",text="Scoreboard" ,font= ('Arial'))
            scoreboard['columns'] = ('player_name', 'player_score', 'pc_score', 'rounds', 'winner','algorithm')

            scoreboard.column("#0", width=0,  stretch=NO)
            scoreboard.column("player_name",anchor=CENTER, width=80)
            scoreboard.column("player_score",anchor=CENTER,width=80)
            scoreboard.column("pc_score",anchor=CENTER,width=80)
            scoreboard.column("rounds",anchor=CENTER,width=80)
            scoreboard.column("winner",anchor=CENTER,width=80)
            scoreboard.column("algorithm",anchor=CENTER,width=80)
            scoreboard.heading("#0",text="",anchor=CENTER)
            scoreboard.heading("player_name",text="Player Name",anchor=CENTER)
            scoreboard.heading("player_score",text="Player Score",anchor=CENTER)
            scoreboard.heading("pc_score",text="Pc Score",anchor=CENTER)
            scoreboard.heading("rounds",text="Rounds",anchor=CENTER)
            scoreboard.heading("winner",text="Winner",anchor=CENTER)
            scoreboard.heading("algorithm",text="Algorithm",anchor=CENTER)

            for i,value in enumerate(listed):
                scoreboard.insert(parent='',index='end',iid=i,text='',
                values=(value[0],value[1],value[2],value[3], value[4],value[5]))


title=Label(frame,text="Καλωσόρισατε στο Scrabble, \n Πληκτρολογίστε το ονομά σας!")
title.pack()
error=Label(frame,text="Δεν πληκτρολόγισες όνομα!",fg="red")
w = Entry( frame,bg="white",width=40)
w.pack(pady= 30)
entry = Entry( frame,bg="white",width=40)
button= ttk.Button(frame, text="Επόμενο", command= get_value)
button.pack()
var = BooleanVar(value=False)
algorithm="smart"




header=Label(frame,name="header",text="" ,font= ('Arial'))
game= ttk.Button(frame, name='gamebutton',text="Παιχνίδι",command=startgame)        
settings= ttk.Button(frame,name='settingsbutton' ,text="Ρυθμίσεις",command=settingsmenu) 
help_button = ttk.Button(frame, name='helpbutton', text="Βοήθεια", command=helpmenu)      
close= ttk.Button(frame,name='closebutton', text="Έξοδος",command=endgame)
label=Label(frame,name="playertext")


def on_close():

    #custom close options, here's one example:
    gameclass.end("")
    screen.destroy()

screen.protocol("WM_DELETE_WINDOW",  on_close)
screen.mainloop()
