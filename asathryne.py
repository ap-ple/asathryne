from random import randint
from stuff import *

class Character():
	
	def __init__(self, name, health, mana, lvl, strength, intelligence, agility, defence, abilities = [], inventory = [], gold = 0):

		self.name = name 
		self.health = health
		self.mana = mana
		self.lvl = lvl
		self.strength = strength
		self.intelligence = intelligence
		self.agility = agility
		self.defence = defence
		self.abilities = abilities
		self.inventory = inventory
		self.gold = gold

	def view_stats(self):

		"""Used to display data about the character to the player"""

		cls()
		print(self)
		print(f"Level {self.lvl}")
		print(f"{self.gold} Gold")
		print(f"Health - {self.health}")
		print(f"Mana - {self.mana}")
		print(f"Strength - {self.strength}")
		print(f"Intelligence - {self.intelligence}")
		print(f"Agility - {self.agility}")
		print(f"Defence - {self.defence}")
		print(f"Abilities - {self.abilities}")
		print(f"Inventory - {self.inventory}")
		dialogue()

	def __repr__(self):

		return self.name

	def __str__(self):

		return self.name

class PlayerCharacter(Character):
	
	def __init__(self, name, class_type, health, mana, lvl, strength, intelligence, agility, defence, abilities = [], inventory = [], gold = 0, xp = 0, abi_points = 0):

		Character.__init__(self, name, health, mana, lvl, strength, intelligence, agility, defence, abilities, inventory, gold)
		self.class_type = class_type
		self.xp = xp
		self.abi_points = abi_points

	def view_stats(self):

		"""Used to display data about the player character to the player"""

		cls()
		print(self)
		print(f"Level {self.lvl} {self.class_type}")
		print(f"{self.gold} Gold")
		print(f"XP - {self.xp}/{(self.lvl + 2) ** 2}")
		print(f"{self.abi_points} ability points left")
		print(f"Health - {self.health}")
		print(f"Mana - {self.mana}")
		print(f"Strength - {self.strength}")
		print(f"Intelligence - {self.intelligence}")
		print(f"Agility - {self.agility}")
		print(f"Defence - {self.defence}")
		print(f"Abilities - {self.abilities}")
		print(f"Inventory - {self.inventory}")
		dialogue()

	def build_char(self):

		"""Used in the beginning to build the player character"""

		while True:
			self.name = dialogue("What is your name, traveller?\n")
			if self.name != "": break
			else: print("You must have have a name in this realm.")

		while True:
			class_pick = dialogue("Choose a class.\n1) Warrior\n2) Sorcerer\n3) Ranger\n4) Paladin\n")
			global weap
			if class_pick == "1":
				dialogue("--- You chose the warrior class, which favors Strength.\n- Courage, above all else, is the first quality of a warrior!\n")
				self.class_type = "Warrior"
				self.strength += 3
				weap = axe
				break
			elif class_pick == "2":
				dialogue("--- You chose the sorcerer class, which favors Intelligence.\n- The true sign of intelligence is not knowledge, but imagination.\n")
				self.class_type = "Sorcerer"
				self.intelligence += 3
				weap = staff
				break
			elif class_pick == "3":
				dialogue("--- You chose the ranger class, which favors Agility.\n- Accuracy comes with great discipline.\n")
				self.class_type = "Ranger"
				self.agility += 3
				weap = bow
				break
			elif class_pick == "4":
				dialogue("--- You chose the paladin class, which favors Defence.\n- To the righteous we bring hope.\n")
				self.class_type = "Paladin"
				self.defence += 3 
				weap = sword
				break
			else:
				print("--- Invalid choice")

	def item_find(self, item):

		"""Used whenever the player character has found an item"""

		while True:
			if item.quest:
				self.inventory.append(item)
				dialogue(f"--- You have recieved {item}, and it has been added to your inventory.\n")
				return
			x = dialogue(f"--- You have recieved a(n) {item}, worth {item.value} gold! Do you take it, or leave it behind? (T/L)\n").upper()
			if x == "T":
				self.inventory.append(item)
				dialogue(f"--- {item} has been added to your inventory.\n")
				return
			if x == "L":
				dialogue(f"--- You left the {item} behind, and {int(0.7 * item.value)} gold has been added to your inventory.\n")
				self.gold += int(0.7 * item.value) #if you leave behind an item, you will recieve 70% of its value in gold
				return
			else:
				print("--- Invalid choice")

	def item_remove(self, item):

		"""Used to remove an item from the player's inventory"""

		for i in self.inventory:
			if i is item:
				dialogue(f"--- {item} has been removed from your inventory.\n")
				self.inventory.remove(item)

	def learn_ability(self):

		"""Used whenever the player character can learn a new ability; only used in lvl_up as of current"""

		while True:
			ability_list = []
			for abi in abilities:
				if abi.max_lvl > abi.lvl:
					if abi.stat == "Strength":
						if self.strength >= abi.minimum_stat:
							ability_list.append(abi)
					elif abi.stat == "Intelligence":
						if self.intelligence >= abi.minimum_stat:
							ability_list.append(abi)
					elif abi.stat == "Agility":
						if self.agility >= abi.minimum_stat:
							ability_list.append(abi)
					elif abi.stat == "Defence":
						if self.defence >= abi.minimum_stat:
							ability_list.append(abi)
			if ability_list == []:
				dialogue("--- There are no avaliable abilities to learn/upgrade.\n")
				return True
			print("--- Choose an ability to learn/upgrade.")
			x = 0
			for abi in ability_list:
				x += 1
				print(f"{x}) {abi} ({abi.lvl}/{abi.max_lvl}): {abi.desc}")
			choice = num_input()
			if choice > x or choice == 0:
				cls()
				print("--- Invalid choice")
				continue
			x = 0
			for abi in ability_list:
				x += 1
				if choice == x:
					cls()
					if abi.lvl == 0: dialogue(f"--- You have learned {abi}.\n")
					else: dialogue(f"--- You have upgraded {abi}.\n")
					self.abilities.append(abi)
					abi.lvl += 1
					self.abi_points -= 1
					return False

	def lvl_up(self):

		"""Whenever the player's xp reaches a certain point, they will level up"""

		while self.xp >= (self.lvl + 2) ** 2:
			self.xp -= (self.lvl + 2) ** 2
			self.lvl += 1
			self.health += 50
			self.mana += 25
			self.abi_points += 1
			dialogue(f"--- You have leveled up to level {self.lvl}! Your power increases.\n")
			points = 3
			while True:
				strength = num_input(f"--- Strength: {self.strength} ({points} points remaining) Add: ")
				if strength > points:
					strength = points
				points -= strength
				self.strength += strength
				if points == 0:
					cls()
					break
				cls()
				intelligence = num_input(f"--- Intelligence: {self.intelligence} ({points} points remaining) Add: ")
				if intelligence > points:
					intelligence = points
				points -= intelligence
				self.intelligence += intelligence
				if points == 0:
					cls()
					break
				cls()
				agility = num_input(f"--- Agility: {self.agility} ({points} points remaining) Add: ")
				if agility > points:
					agility = points
				points -= agility
				self.agility += agility
				if points == 0:
					cls()
					break
				cls()
				defence = num_input(f"--- Defense: {self.defence} ({points} points remaining) Add: ")
				if defence > points:
					defence = points
				points -= defence
				self.defence += defence
				if points == 0:
					cls() 
					break
				cls()
			while self.abi_points != 0:
				if self.learn_ability():
					break

class Item:
	
	def __init__(self, name, value = 0, consumable = False, quest = False):
		
		self.name = name
		self.value = value
		self.consumable = consumable
		self.quest = quest

	def __repr__(self):
		
		return self.name
	
	def __str__(self):

		return self.name

class Ability:
	
	def __init__(self, name, desc, stat, minimum_stat, lvl = 0, max_lvl = 3):
		
		self.name = name
		self.desc = desc
		self.stat = stat
		self.lvl = lvl
		self.max_lvl = max_lvl
		self.minimum_stat = minimum_stat
	
	def __repr__(self):
		
		return self.name
	
	def __str__(self):

		return self.name

"""
character
health - How much damage the character can take before they perish
mana - Determines the character's use of abilities
lvl - Represents the character's power level
strength - Determines the amount of damage the character deals with physical attacks
intelligence - Determines the potency of the character's spells
agility - Determines the accuracy of the character's attacks, and how often they dodge attacks
defence - Determines how much damage the character take from physical attacks
abilities - list of abilities the character can use in battle
inventory - list of items the character carries
gold - currency carried by the character
player character
class - determines what stat you favor; underdeveloped as of current
xp - Gain XP in battle; when you have enough, you will go up one level and you will get to use your skill points.
abi_points - If the player cannot learn abilities at the moment, they will recieve an ability point to use for later.
"""

axe = Item("Axe", 10)
staff = Item("Staff", 10)
bow = Item("Bow", 10)
sword = Item("Sword", 10)
sanctuary_key = Item("Sanctuary Key", quest = True)
pot_health = Item("Health Potion", 20, consumable = True)
pot_mana = Item("Mana Potion", 20, consumable = True)
potions = [pot_health, pot_mana]
weapons = [axe, staff, bow, sword]

stun = Ability(
	name = "Stun",
	desc = "You swing with your weapon, with so much force that the enemy cannot use abilities for 2 turns.",
	stat = "Strength",
	minimum_stat = 8)

fireball = Ability(
	name = "Fireball",
	desc = "You cast a fireball at your enemy, and on impact, it has a chance to burn the enemy.",
	stat = "Intelligence",
	minimum_stat = 8)

sure_shot = Ability(
	name = "Sure Shot",
	desc = "You fire a well-aimed shot from your bow, which can't miss, and deals critical damage.",
	stat = "Agility",
	minimum_stat = 8)

protection = Ability(
	name = "Protection",
	desc = "You summon a magical wall of protection, which prevents half of the damage dealt to you for 3 turns.",
	stat = "Defence",
	minimum_stat = 8)

abilities = [stun, fireball, sure_shot, protection]

player = PlayerCharacter(
	name = "",
	class_type = "",
	health = 50,
	mana = 25,
	lvl = 0,
	strength = 5,
	intelligence = 5,
	agility = 5,
	defence = 5,
	xp = 4,
	gold = 50)

def intro():
	cls()
	print(">>> Asathryne <<<")
	dialogue("Press enter to start.\n")
	player.build_char()
	if dialogue("--- Type 'skip' to skip the tutorial, or press enter to continue\n") == "skip":
		player.item_find(weap)
		player.lvl_up()
	else:
		dialogue(f"Welcome to The Realm of Asathryne, {player}. A kingdom filled with adventure and danger, with much in store for those brave enough to explore it. Of course, nothing a {player.class_type} such as yourself can't handle.")
		dialogue("Oh, of course! Allow me to introduce myself. My name is Kanron, your advisor.")
		dialogue(f"You can't just go wandering off into Asathryne without a weapon. Every {player.class_type} needs a {weap}!")
		player.item_find(weap)
		dialogue("Before you go venturing off into the depths of this realm, you must first master some basic skills.")
		stat_info()
		dialogue("Let's upgrade your stats. For your class, you recieve an extra 3 skill points in the stat that your class favors, and you will recieve 1 level up.")
		player.lvl_up()
		dialogue("Great job! Now that you have learned the basics, it is time you start your journey into the Realm of Asathryne.")
		dialogue("If you ever need me to explain things again, just look for the help option in the menu. Good luck on your journey!")

def stat_info():
	dialogue("Your stats determine your performance in battle, and the abilities you can learn.")
	dialogue("There are 4 main stats: Strength, Intelligence, Agility, and Defense.")
	while True:
		learn_more = dialogue("Do you want to learn more about stats? (Y/N)\n").lower()
		if learn_more == 'y':
			dialogue("Strength increases the amount of damage you deal with physical attacks.")
			dialogue("Intelligence increases the potency of your spells.")
			dialogue("Agility determines the accuracy of your attacks, and how often you dodge attacks.")
			dialogue("Defense determines how much damage you take from physical attacks.")
			dialogue("Your mana determines your use of abilities.")
			dialogue("Your health determines how much damage you can take before you perish.")
			break
		elif learn_more == 'n': break
		else: print("--- Invalid choice")
	dialogue("Let's talk about your level.")
	dialogue("Your level represents how powerful you are, and determines the level of your enemies; when you go up a level, you will recieve 3 skill points to spend on any of the 4 stats, and 1 ability point to learn/upgrade abilities. Additionally, your health and mana will automatically increase.")
	dialogue("You can gain XP (experience points) in battle; when you have enough, you'll go up one level and get to use your skill points.")

king_dialogue = False

def Sanctuary_Gates():
	cls()
	dialogue("--- You travel to the city gates.")
	while True:
		if king_dialogue:
			dialogue("Asathryne Gatekeeper: Halt there, young - ")
			dialogue("Oh. You spoke with the King? I suppose my orders are to let you through then. Here, hand me the key.")
			last_option = dialogue("1) Return to Sanctuary\n2) Go through the gates\n")
			if last_option == "1":
				dialogue("Very well. Return to the town square, and come back here when you are ready.")
				return
			elif last_option == "2":
				dialogue("--- You give the key to the gatekeeper. The gates open, revealing an expansive forest, teeming with otherworldly life.")
				player.item_remove(sanctuary_key)
				dialogue("Good luck out there, traveller.")
				Forest_of_Mysteries()
				return
			else:
				print("--- Invalid choice")
		else:
			break
	dialogue("Asathryne Gatekeeper: Halt there, young traveller! There is a dangerous, dark evil behind these gates. I shall not let you pass, unless you have spoken with the King of Asathryne!")
	while True:
		option_gate = dialogue("Type 'go' to go meet King Brand, or 'exit' to return to the town square.\n").lower()
		if option_gate == "go":
			Sanctuary_Kings_Palace()
			return
		elif option_gate == "exit":
			cls()
			dialogue("--- You return to the town square.")
			return
		else:
			cls()
			gate_random = randint(1, 3)
			if gate_random == 1: dialogue("What are you waiting for? Go on!")
			elif gate_random == 2: dialogue("Don't think standing here will convince me to open this gate.")
			else: dialogue("Brand is waiting for you.")

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
				print("--- Invalid choice")
	dialogue(f"King Brand: At last, a brave {player.class_type} has arisen once more in this kingdom, here on a quest to save the kingdom of Asathryne from the dark evil that lies beyond the gates.")
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
			player.item_find(sanctuary_key)
			dialogue("Fare well, young traveller.")
			king_dialogue = True
			return
		else:
			print("--- Invalid choice")
	while True:
		option_2 = dialogue("Let me ask you a question, traveller. Would you like to hear the Story of Asathryne? (Y/N)\n").lower()
		if option_2 == "n":
			dialogue("Very well, very well, let me see... it's here somewhere... ah! The Key to Asathryne. Take this, young traveller, and good luck!")
			player.item_find(sanctuary_key)
			king_dialogue = True
			return
		elif option_2 == "y":
			for s in king_story:
				dialogue(s)
			dialogue("You will be the one to free us from this crisis.")
			dialogue("Here, take this key; you will need it to open the gate into what remains of Asathryne.")
			player.item_find(sanctuary_key)
			dialogue("Fare well, young traveller.")
			king_dialogue = True
			return
		else:
			print("--- Invalid choice")

def Sanctuary_Apothecary():
	dialogue("--- You travel to the apothecary.")
	dialogue("Welcome to the Apothecary! We have a variety of potions for sale. Take a look at what we have in stock.")
	while True:
		print(f"--- You have {player.gold} gold.")
		x = 1
		for p in potions:
			print(f"{x}) {p}: {p.value} gold")
			x += 1
		print(f"{x}) Leave")
		choice = num_input()
		if choice == len(potions) + 1:
			cls()
			return
		if choice <= 0 or choice > len(potions):
			cls()
			print("Invalid choice")
			continue
		pot_choice = potions[choice - 1]
		if pot_choice.value > player.gold:
			cls()
			print("Insufficient funds")
			continue
		player.gold -= pot_choice.value
		player.inventory.append(pot_choice)
		cls()
		print(f"You bought a {pot_choice} for {pot_choice.value} gold.")

def Sanctuary_Blacksmith():
	dialogue("--- You travel to the blacksmith.")
	dialogue("Hello there, traveller! You look like you could use some armor, and a reliable weapon, too. Step into my blacksmith shop and take a look at my many wares!\n")
	while True:
		print(f"--- You have {player.gold} gold.")
		x = 1
		for w in weapons:
			print(f"{x}) {w}: {w.value} gold")
			x += 1
		print(f"{x}) Leave")
		choice = num_input()
		if choice == len(weapons) + 1:
			cls()
			return
		if choice <= 0 or choice > len(weapons):
			cls()
			print("Invalid choice")
			continue
		weap_choice = weapons[choice - 1]
		if weap_choice.value > player.gold:
			cls()
			print("Insufficient funds")
			continue
		player.gold -= weap_choice.value
		player.inventory.append(weap_choice)
		cls()
		print(f"You bought a {weap_choice} for {weap_choice.value} gold.")
def Sanctuary_Town_Square():
	dialogue("--- You arrive at Sanctuary's town square.\n")
	while True:
		option = dialogue("Sanctuary\n1) The Apothecary\n2) The King's Palace\n3) The Gates\n4) The Blacksmith\n5) Help\n6) View Character\n")
		if option == "1": Sanctuary_Apothecary()
		elif option == "2":	Sanctuary_Kings_Palace()
		elif option == "3": Sanctuary_Gates()
		elif option == "4":	Sanctuary_Blacksmith()
		elif option == "5":	stat_info()
		elif option == "6":	player.view_stats()
		else: print("Enter a number to travel to the designated location.")

def Forest_of_Mysteries():
	dialogue("Forest\n")
	return

intro()
Sanctuary_Town_Square()
