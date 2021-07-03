import random, time
from threading import Timer

running = True
timeTrialRunning = False

# opens highscore file defined by directory (parameter)
# appends each value to a new table with scores and names
# sorts the table, and returns it to be used
def setupHSTable(d):
    table = []
    file = open(d)
    with file as f:
        for item in f:
            table.append([i for i in item.split(',')])
    for i in range(5):
        b = table[i]
        b[0] = int(b[0])
        b.pop()
    file.close()
    table = sorted(table,reverse=True, key=lambda x: x[0])
    return table

# prints highscores using table previously set up
def printHS(t):
    print("These are the current highscores: ")
    for i in range(5):
        row = t[i]
        print((i + 1),".   ",row[1],"",row[0])

# saves highscores back to the file formatted the same way
def saveHS(d, hs):
    file = open(d,"w")
    for i in range(5):
        row = hs[i]
        p = (str(row[0]) + "," + str(row[1]) + ",\n")
        file.write(p)
    file.close()

# loads list of words from file
def loadWords():
    file = open("words.txt","r")
    words = file.readlines()
    file.close()
    return words

# picks random word and splits into individual characters
def pickWord():
    global words
    r = random.randint(0, (len(words) - 1))
    word = words[r]
    word = word.replace("\n","")
    word = list(word)
    return word

# resets/creates a blank grid (as 2d array)
def resetGrid():
    grid = [[" ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " "]]
    grid[4] = ["_"]*7
    return grid

# prints current grid
def printGrid(grid):
    for row in grid:
        print("".join(*zip(*row)))

# updates grid
def updateGrid(grid, stage, easy):
    if easy:
        if stage == 1:
            grid[4][0] = "|"
        elif stage == 2:
            grid[4][1] = "\\"
        elif stage == 3:
            grid[3][0] = "|"
        elif stage == 4:
            grid[2][0] = "|"
        elif stage == 5:
            grid[1][0] = "|"
        elif stage == 6:
            grid[0][1] = "_"
        elif stage == 7:
            grid[0][2] = "_"
        elif stage == 8:
            grid[0][3] = "_"
        elif stage == 9:
            grid[0][4] = "_"
        elif stage == 10:
            grid[0][5] = "_"
        elif stage == 11:
            grid[1][5] = "O"
        elif stage == 12:
            grid[2][5] = "|"
        elif stage == 13:
            grid[3][4] = "/"
        elif stage == 14:
            grid[3][6] = "\\"
        elif stage == 15:
            grid[2][4] = "-"
        elif stage == 16:
            grid[2][6] = "-"

    else:
        if stage == 1:
            grid[1][0] = "|"
            grid[2][0] = "|"
            grid[3][0] = "|"
            grid[4][0] = "|"
        elif stage == 2:
            grid[0][1] = "_"
            grid[0][2] = "_"
            grid[0][3] = "_"
            grid[0][4] = "_"
            grid[0][5] = "_"
        elif stage == 3:
            grid[1][5] = "O"
        elif stage == 4:
            grid[2][5] = "|"
        elif stage == 5:
            grid[3][4] = "/"
        elif stage == 6:
            grid[3][6] = "\\"
        elif stage == 7:
            grid[2][4] = "-"
        elif stage == 8:
            grid[2][6] = "-"
    return grid

# checks if an entered letter matches any letter in the word
def checkLetter(word, choice, curWord, used, fails, correct):
    failed = True
    for i in range(len(word)):
        if choice == word[i]:
            if curWord[i] == "_ ":
                correct += 1
            curWord[i] = choice + " "
            failed = False
    if failed:
        print("Incorrect")
        fails += 1
        used += choice
    return curWord, fails, correct, used

# runs original mode
def original(easy, z):
    grid = resetGrid()
    word = pickWord()
    length = len(word)
    curWord = ["_ "]
    display = ""
    usedLetters = ""
    fails = 0
    correct = 0
    for i in range(length - 1):
        curWord.append("_ ")
    while fails < z and correct < len(word):
        grid = updateGrid(grid, fails, easy)
        printGrid(grid)
        display = ""
        for i in range(len(curWord)):
            display += curWord[i]
        print("\n" + display)
        print("\nIncorrect letters:",usedLetters)
        while True:
            choice = input("\nEnter a letter: ")
            if len(choice) == 1:
                break
            else:
                print("Please enter a single letter!!")
        curWord, fails, correct, usedLetters = checkLetter(word, choice, curWord, usedLetters, fails, correct)
    display = ""
    for i in range(len(curWord)):
        display += curWord[i]
    print("\n" + display)
    display = ""
    for i in range(len(word)):
            display += word[i]
    if fails == z:
        print("\n\n\n---- TOO BAD! ----")
        print("The word was '" + display + "'")
        grid = updateGrid(grid, fails, easy)
        printGrid(grid)
    else:
        print("\n\n---- YOU WON! ----")
        print("You guessed the word '" + display + "'")

# runs quickfire mode
def quickfire():
    hs = setupHSTable("quickfireHS.txt")
    printHS(hs)
    mLives = 50
    fails = 0
    total = 0
    while fails < mLives:
        word = pickWord()
        length = len(word)
        curWord = ["_ "]
        display = ""
        usedLetters = ""
        correct = 0
        for i in range(length - 1):
            curWord.append("_ ")
        while correct < len(word) and fails < mLives:
            lives = mLives - fails
            print("\nYou have",lives,"lives left\n")
            display = ""
            for i in range(len(curWord)):
                display += curWord[i]
            print("\n" + display)
            print("\nIncorrect letters:",usedLetters)
            while True:
                choice = input("\nEnter a letter: ")
                if len(choice) == 1:
                    break
                else:
                    print("Please enter a single letter!!")
            curWord, fails, correct, usedLetters = checkLetter(word, choice, curWord, usedLetters, fails, correct)
        if fails < mLives:
            display = ""
            for i in range(len(curWord)):
                display += curWord[i]
            print("\n" + display)
            total += 1
            print("\nYou have currently completed",total,"words.\n")
    print("\n\n---- YOU RAN OUT OF LIVES ----\n")
    print("Your final score was",total,"words.")
    for i in range(5):
        row = hs[i]
        if total > row[0]:
            name = input("\nWhat is your name?: ")
            hs.insert(i, [total, name])
            hs.pop()
            break
    printHS(hs)
    saveHS("quickfireHS.txt", hs)

def endTimeTrial():
    global timeTrialRunning
    timeTrialRunning = False

# runs time trial mode
def timetrial():
    global timeTrialRunning
    timeTrialRunning = True
    hs = setupHSTable("timetrialHS.txt")
    printHS(hs)
    total = 0
    print("You have 3 minutes starting...")
    time.sleep(3)
    print("\n\nNOW!!\n\n")
    t = Timer(60, endTimeTrial)
    t.start()
    while timeTrialRunning:
        word = pickWord()
        length = len(word)
        curWord = ["_ "]
        display = ""
        usedLetters = ""
        correct = 0
        fails = 0
        for i in range(length - 1):
            curWord.append("_ ")
        while correct < len(word) and timeTrialRunning:
            print("\nYou have currently completed",total,"words.\n")
            display = ""
            for i in range(len(curWord)):
                display += curWord[i]
            print("\n" + display)
            print("\nIncorrect letters:",usedLetters)
            while True:
                choice = input("\nEnter a letter: ")
                if len(choice) == 1:
                    break
                else:
                    print("Please enter a single letter!!")
            curWord, fails, correct, usedLetters = checkLetter(word, choice, curWord, usedLetters, fails, correct)
        total += 1
    t.cancel()
    print("\n\n---- YOU RAN OUT OF TIME ----\n")
    print("Your final score was",(total - 1),"words.")
    for i in range(5):
        row = hs[i]
        if total > row[0]:
            name = input("\nWhat is your name?: ")
            hs.insert(i, [total, name])
            hs.pop()
            break
    printHS(hs)
    saveHS("timetrialHS.txt", hs)

def Help():
    print("This is hangman, a game where you must guess a word but with only limited choices, as the more you get incorrect, the closer you get to being hanged.")
    print("Original:")
    print("Original is simply the original version of hangman.")
    print("Quickfire:")
    print("In quickfire mode, you have 30 lives and must solve as many words as possible before losing your lives.")
    print("Time trial:")
    print("As the name suggests, in this mode you have infinite lives and must solve as many words as possible before the time runs out.")
    print("Easy:")
    print("An easier version of the original, with double the attempts. Wow!")

# menu to choose mode / exit
def menu():
    # prints options
    print("\nPlease enter the number of your choice below: ")
    print("1. Original")
    print("2. Quickfire")
    print("3. Time trial")
    print("4. Easy")
    print("5. Help")
    print("6. Exit")
    # requests input
    choice = input("")
    # uses input to determine what to do
    if choice == "1":
        original(False, 8)
    elif choice == "2":
        quickfire()
    elif choice == "3":
        timetrial()
    elif choice == "4":
        original(True, 16)
    elif choice == "5":
        Help()
    else:
        # exits
        global running
        running = False

words = loadWords()
print("---------- Welcome to the Hangman Program! ----------")

# initiates program
while running:
    menu()
