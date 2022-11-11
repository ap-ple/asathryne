import os
import time
import keyboard
from getpass import getpass

delay = 0.15

#clears the screen
def clear():
    print('\n' * 1000) #faster, but leaves behind copies and displays text at the bottom of the screen
    #os.system('cls' if os.name == 'nt' else 'clear') #slower

#Like input, but only accepts numbers; returns number in integer form, or 0 if the input is not a number
def num_input(string=''):
    x = input(string)
    return int(x) if x.isdecimal() else 0

#Like input, but clears after the input is taken
def clear_input(string=''):
    x = input(string)
    clear()
    return x

#Allows dialogue, displays text and waits until enter is pressed, then clears
def dialogue(string=''):
    getpass(string)
    clear()

#Asks the user to choose from a list by number input; returns the number chosen
def choose_number(prompt, choices, error = '--- Invalid choice'):
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

#Asks the user to choose from a list; returns the number chosen
def choose(prompt, choices, choice = 1, ret = False):
    while True:
        print(prompt)
        for i, c in enumerate(choices, 1):
            print(f' {">" if i == choice else "-"} {c}')
        time.sleep(delay)
        pressed = keyboard.read_key(True)
        if pressed == 'up':
            if choice > 1:
                choice -= 1
        elif pressed == 'down':
            if choice < len(choices):
                choice += 1
        elif pressed == 'enter':
            time.sleep(delay)
            clear()
            if ret:
                return choices[choice - 1]
            return choice
        clear()

if __name__ == '__main__':
    dialogue('This is the stuff module.')
