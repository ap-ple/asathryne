import os

#a shorter version of system('cls')
def clear():
    os.system("cls" if os.name == "nt" else "clear")

#Like input, but only accepts numbers; returns number in integer form, or 0 if the input is not a number
def num_input(string=""):
    x = input(string)
    return int(x) if x.isdecimal() else 0

#Like input, but clears after the input is taken
def dialogue(string=""):
    x = input(string)
    clear()
    return x

#Asks the user to choose from a list; returns the number chosen
def choose(prompt, choices, error = '--- Invalid choice'):
    while True:
        print(prompt)
        for i, c in enumerate(choices, 1):
            print(f'{i}) {c}')
        choice = num_input()
        clear()
        if choice > len(choices) or choice <= 0:
            print(error)
            continue
        return choice

#returns a string of the simplest radical form of the square root of a number
def radical(num):
    numlist = []
    while True: 
        for n in range(2, 999):
            if num % (n ** 2) == 0:
                num /= (n ** 2)
                numlist.append(n)
                break
        else:
            break
    newnum = 1
    for n in numlist:
        newnum *= n
    if newnum == 1:
        return f"√{int(num)}"
    elif num == 1:
        return newnum
    else:
        return f"{newnum}√{int(num)}"
