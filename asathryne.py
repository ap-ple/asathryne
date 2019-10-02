from os import system
from random import randint
from stuff import *

character = {
  "Name": "",
  "Class": "",
  "AbiPts": 0, #If the player cannot learn abilities at the moment, they will recieve an ability point to use for later.
  "HP": 50, #How much damage you can take before you perish.
  "AP": 25, #Determines your use of abilities
  "XP": 4, #Gain XP in battle; when you have enough, you will go up one level and you will get to use your skill points.
  "Lvl": 0, #Represents your power level, and determines the level of your enemies; when you go up a level, you will recieve 5 skill points
  "Str": 5, #Determines the amount of damage you deal with physical attacks
  "Int": 5, #Determines the potency of your spells
  "Agi": 5, #Determines the accuracy of your attacks, and how often you dodge attacks
  "Def": 5, #Determines how much damage you take from physical attacks
  "Abilities": [],
  "Inventory": [],
  "Gold": 50
}

def intro():
  cls()
  print(">>> Asathryne <<<")
  dialogue("Press enter to start.")
  
  while True:
    character["Name"] = dialogue("""What is your name, traveller?
    """)
    if character["Name"] != "":
      break
    else:
      print("You must have have a name in this realm.")

  while True:
    print("""Choose a class.
1) Warrior
2) Sorcerer
3) Ranger
4) Paladin""")
    Class = dialogue()
    cls()
    if Class == "1":
      dialogue("""--- You chose the warrior class, which favors Strength.
    - Courage, above all else, is the first quality of a warrior!
  """)
      character["Class"] = "Warrior"
      break
    elif Class == "2":
      dialogue("""--- You chose the sorcerer class, which favors Intelligence.
    - The true sign of intelligence is not knowledge, but imagination.
  """)
      character["Class"] = "Sorcerer"
      break
    elif Class == "3":
      dialogue("""--- You chose the ranger class, which favors Agility.
    - Accuracy comes with great discipline.
  """)
      character["Class"] = "Ranger"
      break
    elif Class == "4":
      dialogue("""--- You chose the paladin class, which favors Defense.
    - To the righteous we bring hope.
  """)
      character["Class"] = "Paladin"
      break
    else:
      print("--- Type one of the numbers to pick your class.")
  
  if character["Class"] == "Warrior":
    character["Str"] += 3
    weap = items["Axe"]
  elif character["Class"] == "Sorcerer":
    character["Int"] += 3
    weap = items["Staff"]
  elif character["Class"] == "Ranger":
    character["Agi"] += 3
    weap = items["Bow"]
  elif character["Class"] == "Paladin":
    character["Def"] += 3 
    weap = items["Sword"]

  if dialogue("--- Type 'skip' to skip the tutorial, or press enter to continue ") == "skip":
    item_find(weap)
    lvlup()
  else:
    dialogue(f"Welcome to The Realm of Asathryne, {character['Name']}. A kingdom filled with adventure and danger, with much in store for those brave enough to explore it. Of course, nothing a {character['Class']} such as yourself can't handle.")
    dialogue("Oh, of course! Allow me to introduce myself. My name is Kanron, your advisor.")
    dialogue(f"You can't just go wandering off into Asathryne without a weapon. Every {character['Name']} needs a {weap['Name']}!")
    item_find(weap)
    dialogue("Before you go venturing off into the depths of this realm, you must first master some basic skills.")
    Help()
    dialogue("Let's upgrade your stats. For your character, you recieve an extra 3 skill points in the stat that your class favors, and you will recieve 1 level up.")
    lvlup()
    dialogue("Great job! Now that you have learned the basics, it is time you start your journey into the Realm of Asathryne.")
    dialogue("If you ever need me to explain things again, just look for the help option in the menu. Good luck on your journey!")

item_1 = {
  "Name": "Axe",
  "Value": 10,
  "Cons": False, #consumable
  "Quest": False #quest item
}

item_2 = {
  "Name": "Staff",
  "Value": 10,
  "Cons": False,
  "Quest": False
}

item_3 = {
  "Name": "Bow",
  "Value": 10,
  "Cons": False,
  "Quest": False
}

item_4 = {
  "Name": "Sword",
  "Value": 10,
  "Cons": False,
  "Quest": False
}

item_5 = {
  "Name": "Sanctuary Key",
  "Value": 0,
  "Cons": False,
  "Quest": True
}

item_6 = {
  "Name": "Health Potion",
  "Value": 20,
  "Cons": True,
  "Quest": False
}

item_7 = {
  "Name": "Mana Potion",
  "Value": 20,
  "Cons": True,
  "Quest": False
}

abi_1 = {
  "Name": "Stun",
  "Desc": "You swing with your weapon, with so much force that the enemy cannot use abilities for 2 turns.",
  "Type": "Str",
  "Lvl": 0,
  "Max": 3,
  "Stat": 8,
  "Req": True
}

abi_2 = {
  "Name": "Fireball",
  "Desc": "You cast a fireball at your enemy, and on impact, it has a chance to burn the enemy.",
  "Type": "Int",
  "Lvl": 0,
  "Max": 3,
  "Stat": 8,
  "Req": True
}

abi_3 = {
  "Name": "Sure Shot",
  "Desc": "You fire a well-aimed shot from your bow, which can't miss, and deals critical damage.",
  "Type": "Agi",
  "Lvl": 0,
  "Max": 3,
  "Stat": 8,
  "Req": True
}

abi_4 = {
  "Name": "Protection",
  "Desc": "You summon a magical wall of protection, which prevents half of the damage dealt to you for 3 turns.",
  "Type": "Def",
  "Lvl": 0,
  "Max": 3,
  "Stat": 8,
  "Req": True
}

items = {
  "Axe": item_1,
  "Staff": item_2,
  "Bow": item_3,
  "Sword": item_4,
  "Sanctuary Key": item_5,
}

abilities = [abi_1, abi_2, abi_3, abi_4]

def learn_ability(): #only used in lvlup, but might be used in other places later on
  while True:
    choice = 0
    ability_list = []
    for a in abilities:
      if a["Max"] > a["Lvl"]:
        if a["Type"] == "Str":
          if character["Str"] >= a["Stat"]:
            ability_list.append(a)
        elif a["Type"] == "Int":
          if character["Int"] >= a["Stat"]:
            ability_list.append(a)
        elif a["Type"] == "Agi":
          if character["Agi"] >= a["Stat"]:
            ability_list.append(a)
        elif a["Type"] == "Def":
          if character["Def"] >= a["Stat"]:
            ability_list.append(a)
    if ability_list == []:
      dialogue("--- There are no avaliable abilities to learn/upgrade.")
      return True
    print("--- Choose an ability to learn/upgrade.")
    for a in ability_list:
      choice += 1
      print(f"{choice}) {a['Name']} ({a['Lvl']}/{a['Max']}): {a['Desc']}")
    x = num_input(" ")
    if x > choice or x == 0:
      cls()
      print("--- Type the corresponding number to learn an ability.")
    else:	
      choice = 0
      for a in ability_list:
        choice += 1
        if x == choice:
          cls()
          if a["Lvl"] == 0:
          	dialogue(f"--- You have learned {a['Name']}.")
          else:
            dialogue(f"--- You have upgraded {a['Name']}.")
          character["Abilities"].append(a)
          a["Lvl"] += 1
          character["AbiPts"] -= 1
          return False

def item_find(item): #whenever you find an item, it will give you the option to add it to your inv or leave it
  while True:
    if item["Quest"]:
      character["Inventory"].append(item)
      dialogue(f"--- You have recieved {item['Name']}, and it has been added to your inventory.")
      return
    x = dialogue(f"--- You have recieved a(n) {item['Name']}, worth {item['Value']} gold! Do you take it, or leave it behind? (T/L) ").upper()
    if x == "T":
      character["Inventory"].append(item)
      dialogue(f"--- {item['Name']} has been added to your inventory.")
      return
    if x == "L":
      dialogue(f"--- You left the {item['Name']} behind, and {int(0.7 * item['Value'])} gold has been added to your inventory.")
      character["Gold"] += int(0.7 * item["Value"]) #if you leave behind an item, you will recieve 70% of its value in gold
      return
    else:
      print(" --- Type 'T' to take the item, or 'L' to leave it.")

def lvlup(): #Whenever the player's xp reaches a certain point, they will level up
  while character["XP"] >= (character["Lvl"] + 2) ** 2:
    character["XP"] -= (character["Lvl"] + 2) ** 2
    character["Lvl"] += 1
    character["HP"] += 50
    character["AP"] += 25
    character["AbiPts"] += 1
    dialogue(f"--- You have leveled up to level {character['Lvl']}! Your power increases.")
    points = 3
    while True:
      strength = num_input(f"--- Strength: {character['Str']} ({points} points remaining) Add:")
      if strength > points:
        strength = points
      points -= strength
      character["Str"] += strength
      if points == 0:
        cls()
        break
      cls()
      intelligence = num_input(f"--- Intelligence: {character['Int']} ({points} points remaining) Add:")
      if intelligence > points:
        intelligence = points
      points -= intelligence
      character["Int"] += intelligence
      if points == 0:
        cls()
        break
      cls()
      agility = num_input(f"--- Agility: {character['Agi']} ({points} points remaining) Add:")
      if agility > points:
        agility = points
      points -= agility
      character["Agi"] += agility
      if points == 0:
        cls()
        break
      cls()
      defense = num_input(f"--- Defense: {character['Def']} ({points} points remaining) Add:")
      if defense > points:
        defense = points
      points -= defense
      character["Def"] += defense
      if points == 0:
        cls() 
        break
      cls()
    while character["AbiPts"] != 0:
      if learn_ability():
        break

def Help():
  dialogue("Your stats determine your performance in battle, and the abilities you can learn.")
  dialogue("There are 4 main stats: Strength, Intelligence, Agility, and Defense.")
  while True:
    learn_more = dialogue("Do you want to learn more about stats? (Y/N): ").lower()
    if learn_more == 'y':
      dialogue("Strength increases the amount of damage you deal with physical attacks.")
      dialogue("Intelligence increases the potency of your spells.")
      dialogue("Agility determines the accuracy of your attacks, and how often you dodge attacks.")
      dialogue("Defense determines how much damage you take from physical attacks.")
      dialogue("Your AP (action points) determine your use of abilities.")
      dialogue("Your HP (health points) determine how much damage you can take before you perish.")
      break
    elif learn_more == 'n':
      break
    else:
      print("Type 'Y' or 'N'.")
  dialogue("Let's talk about your level.")
  dialogue("Your level represents how powerful you are, and determines the level of your enemies; when you go up a level, you will recieve 3 skill points to spend on any of the 4 stats, and 1 ability point to learn/upgrade abilities. Additionally, your HP and AP will automatically increase.")
  dialogue("You can gain XP (experience points) in battle; when you have enough, you'll go up one level and get to use your skill points.")

def item_remove(item):
  for i in character["Inventory"]:
    if i == item:
      dialogue(f"--- {item['Name']} has been removed from your inventory.")
      character["Inventory"].remove(item)

def view_char():
  for x in character:
    print(f"{x}: {character[x]}")
  dialogue()

king_dialogue = False

def Sanctuary_Gates():
  cls()
  dialogue("--- You travel to the city gates.")
  while True:
    if king_dialogue:
      dialogue("Asathryne Gatekeeper: Halt there, young - ")
      dialogue("Oh. You spoke with the King? I suppose my orders are to let you through then. Here, hand me the key.")
      last_option = dialogue("""1) Return to Sanctuary
2) Go through the gates""")
      if last_option == "1":
        dialogue("Very well. Return to the town square, and come back here when you are ready.")
        return
      elif last_option == "2":
        dialogue("--- You give the key to the gatekeeper. The gates open, revealing an expansive forest, teeming with otherworldly life.")
        item_remove(items["Sanctuary Key"])
        dialogue("Good luck out there, traveller.")
        Forest_of_Mysteries()
        return
      else:
        print("Type 1 or 2")
    else:
      break
  dialogue("Asathryne Gatekeeper: Halt there, young traveller! There is a dangerous, dark evil behind these gates. I shall not let you pass, unless you have spoken with the King of Asathryne!")
  while True:
    option_gate = dialogue("Type 'go' to go meet King Brand, or 'exit' to return to the town square. ").lower()
    if option_gate == "go":
      Sanctuary_Kings_Palace()
      return
    elif option_gate == "exit":
      cls()
      dialogue("You return to the town square.")
      return
    else:
      cls()
      gate_random = randint(1, 3)
      if gate_random == 1:
        dialogue("What are you waiting for? Go on!")
      elif gate_random == 2:
        dialogue("Don't think standing here will convince me to open this gate.")
      else:
        dialogue("Brand is waiting for you.")

def Sanctuary_Kings_Palace():
  global king_dialogue
  king_story = [
    "Very well. Go ahead and take a seat.",
    "Now, Asathryne once was a kingdom filled with happiness and peace, ruled by Emperor Verandus.",
    "Until one day, an evil never before seen, arrived in Asathryne and tore the realm apart, leaving nothing but a barren wasteland.",
    "Sanctuary became the only thriving town left in the land.",
    "The horrid evil killed the emperor and kidnapped his daughter, our future princess. She was one of the most powerful beings in Asathryne.",
    "But this was twenty years ago. Much longer ago, when we had a fighting chance against the dark forces.",
    "We have long waited for a courageous adventurer who would be worthy enough to venture into the depths of Asathryne and rescue us from this terror."
    ]
  dialogue("--- You travel to the king's palace.")
  if king_dialogue:
    dialogue("King Brand: Hello, young traveller.")
    while True:
      king_story_repeat = dialogue("Do you wish to hear the story of Asathryne? (Y/N): ").lower()
      if king_story_repeat == "y":
        for s in king_story:
          dialogue(s)
        return
      elif king_story_repeat == "n":
        dialogue("Oh well, maybe for another day. Fare well, traveller!")
        return
      else:
        print("Type 'Y' or 'N'")
  dialogue(f"King Brand: At last, a brave {character['Class']} has arisen once more in this kingdom, here on a quest to save the kingdom of Asathryne from the dark evil that lies beyond the gates.")
  dialogue("Tell me young traveller, what do you seek from me?")
  while True:
    option_1 = dialogue("""1) The gate keeper has sent me to meet you
2) I'm here to learn about Asathryne
""")
    if option_1 == "1":
      dialogue("Ah, the gate keeper. He forbids anyone entry to the rest of Asathryne, simply because he wants to protect them.")
      break
    elif option_1 == "2":
      for s in king_story:
        dialogue(s)
      dialogue("You will be the one to free us from this crisis.")
      dialogue("Here, take this key; you will need it to open the gate into what remains of Asathryne.")
      item_find(items["Sanctuary Key"])
      dialogue("Fare well, young traveller.")
      king_dialogue = True
      return
    else:
      print("Type 1 or 2")
  while True:
    option_2 = dialogue("Let me ask you a question, traveller. Would you like to hear the Story of Asathryne? (Y/N)").lower()
    if option_2 == "n":
      dialogue("Very well, very well, let me see... it's here somewhere... ah! The Key to Asathryne. Take this, young traveller, and good luck!")
      item_find(items["Sanctuary Key"])
      king_dialogue = True
      return
    elif option_2 == "y":
      for s in king_story:
        dialogue(s)
      dialogue("You will be the one to free us from this crisis.")
      dialogue("Here, take this key; you will need it to open the gate into what remains of Asathryne.")
      item_find(items["Sanctuary Key"])
      dialogue("Fare well, young traveller.")
      king_dialogue = True
      return
    else:
      print("Type 'Y' or 'N'")

def Sanctuary_Apothecary():
  dialogue("--- You travel to the apothecary.")
  dialogue("Welcome to the Apothecary! We have a variety of potions for sale. Take a look at what we have in stock.")
  while True:
    print(f"--- You have {character['Gold']} gold.")
    dialogue("Sorry, there's nothing for sale today. Come back later!")
    return

def Sanctuary_Blacksmith():
  dialogue("--- You travel to the blacksmith.")
  dialogue("Hello there, traveller! You look like you could use some armor, and a reliable weapon, too. Step into my blacksmith shop and take a look at my many wares!")
  while True:
    print(f"--- You have {character['Gold']} gold.")
    dialogue("Sorry, there's nothing for sale today. Come back later!")
    return

def Sanctuary_Town_Square():
  dialogue("--- You arrive at Sanctuary's town square.")
  while True:
    option = dialogue("""Sanctuary
1) The Apothecary
2) The King's Palace
3) The Gates
4) The Blacksmith
5) Help
6) View Character
""")
    if option == "1":
    	Sanctuary_Apothecary()
    elif option == "2":
    	Sanctuary_Kings_Palace()
    elif option == "3":
    	Sanctuary_Gates()
    elif option == "4":
      Sanctuary_Blacksmith()
    elif option == "5":
      Help()
    elif option == "6":
      view_char()
    else:
    	print("Enter a number to travel to the designated location.")

def Forest_of_Mysteries():
  dialogue("Forest")
  return
    
intro()
Sanctuary_Town_Square()
