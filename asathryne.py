from random import randint
import simplejson
import os
from jsonpickle import encode, decode
from stuff import clear, dialogue, num_input

version = '0.0.2'
bugs = (
'Stun deals damage but does not stun',
'Protection has no effect', 
'Potions are unusable', 
'Weapons cannot be equipped/unequipped')

'''
Roadmap

now:
multiple enemies/ally based combat
status effects for combat
choices function, replace all current choice loops with this (maybe not)
revamp items
	- active items
	- equipping weapons
	- item requirements like classes, eg bows for rangers
revamp classes
	- subclasses

later:
add followers/allies
add more abilities 
	- use global targeting like all, all_ally, all_enemy
	- use passives and actives
outsource creative writing and worldbuilding
multiplayer?
	- pvp
	- co-op
'''

class Character():
	
	def __init__(self, name, health, mana, lvl, strength, intelligence, agility, defence, xp, gold, weap, abilities = [], inventory = []):

		self.name = name 
		self.health = health
		self.mana = mana
		self.lvl = lvl
		self.strength = strength
		self.intelligence = intelligence
		self.agility = agility
		self.defence = defence
		self.xp = xp
		self.gold = gold
		self.weap = weap
		self.abilities = abilities
		self.inventory = inventory

	def view_stats(self):

		'''Used to display data about the character to the player'''

		clear()
		print(self)
		print(f'Level {self.lvl}')
		print(f'{self.xp} xp')
		print(f'{self.gold} Gold')
		print(f'Health - {self.health}')
		print(f'Mana - {self.mana}')
		print(f'Strength - {self.strength}')
		print(f'Intelligence - {self.intelligence}')
		print(f'Agility - {self.agility}')
		print(f'Defence - {self.defence}')
		print(f'Weapon - {self.weap} ({self.weap.damage[0]}-{self.weap.damage[1]} damage)')
		print(f'Abilities - {self.abilities}')
		print(f'Inventory - {self.inventory}')
		dialogue()

	def attack(self, target, damage_multiplier = 1, accuracy_multiplier = 1):

		'''Sets the basic attack for all characters; expanded upon through abilities'''

		class Attack:

			def __init__(self, hit, damage):

				self.hit = hit
				self.damage = damage

		if randint(1, 100) < (self.agility / (self.agility + target.agility)) * 100 * accuracy_multiplier:
			hit = True
			damage = int(self.strength / (self.strength + target.defence) * randint(*self.weap.damage) * damage_multiplier)
		else:
			hit = False
			damage = 0
		return Attack(hit, damage)

	def __repr__(self):

		return self.name

	def __str__(self):

		return self.name

class PlayerCharacter(Character):
	
	def __init__(self):

		super().__init__(name = '', health = 50, mana = 25, lvl = 0, strength = 5, intelligence = 5, agility = 5, defence = 5, xp = 4, gold = 50, weap = '')
		self.progress = {'area': '', 'king_dialogue': False, 'gates_dialogue': False, 'gates_unlocked': False}
		self.class_type = ''
		self.abi_points = 0

	def view_stats(self):

		'''Used to display data about the player character to the player'''

		clear()
		print(self)
		print(f'Level {self.lvl} {self.class_type}')
		print(f'{self.gold} Gold')
		print(f'XP - {self.xp}/{(self.lvl + 2) ** 2}')
		print(f'{self.abi_points} ability points left')
		print(f'{self.health} Health')
		print(f'{self.mana} Mana')
		print(f'Strength - {self.strength}')
		print(f'Intelligence - {self.intelligence}')
		print(f'Agility - {self.agility}')
		print(f'Defence - {self.defence}')
		print(f'Weapon - {self.weap} ({self.weap.damage[0]}-{self.weap.damage[1]} damage)')
		print(f'Abilities - {self.abilities}')
		print(f'Inventory - {self.inventory}')
		dialogue()

	def build_char(self):

		'''Used in the beginning to build the player character'''

		while True:
			self.name = dialogue('What is your name, traveller?\n')
			if self.name != '':
				break
			else: 
				print('You must have have a name in this realm.')

		while True:
			print('Choose a class.')
			for i, c in enumerate(classes, 1):
				print(f'{i}) {c}')
			class_pick = num_input()
			clear()
			for i, c in enumerate(classes, 1):
				if class_pick == i:
					dialogue(f'--- You chose the {c} class, which favors {c.stat}.\n')
					setattr(self, c.stat, getattr(self, c.stat) + 3)
					self.class_type = c
					self.inventory.append(c.weap)
					return
			print('--- Invalid choice')

	def equip(self, weapon):

		'''Used to equip a weapon'''

		if weapon in self.inventory:
			self.inventory.remove(weapon)
			self.weap = weapon
			dialogue(f'--- {weapon} has been equipped.')
			return True
		return False

	def item_remove(self, item):

		'''Used to remove an item from the player's inventory'''

		if item in self.inventory:
			dialogue(f'--- {item} has been removed from your inventory.\n')
			self.inventory.remove(item)
			return True
		return False

	def learn_ability(self):

		'''Used whenever the player character can learn a new ability; only used in lvl_up as of current'''

		ability_list = [abi for abi in self.abilities if abi.max_lvl > abi.lvl and abi.check(self)]
		for abi in abilities: 
			if abi.check(self):
				if self.abilities == []:
					ability_list.append(abi)
				else:
					if all(a.name != abi.name for a in self.abilities):
						ability_list.append(abi)
		if ability_list == []:
			dialogue('--- There are no avaliable abilities to learn/upgrade.\n')
			return False
		while True:
			print(f'--- You have {len(ability_list)} abilities to learn/upgrade.')
			for i, abi in enumerate(ability_list, 1):
				print(f'{i}) {abi} ({abi.lvl}/{abi.max_lvl}): {abi.desc}')
			choice = num_input()
			clear()
			if choice > len(ability_list) or choice <= 0:
				print('--- Invalid choice')
				continue
			for i, abi in enumerate(ability_list, 1):
				if choice == i:
					if abi.lvl == 0: 
						dialogue(f'--- You have learned {abi}.\n')
						self.abilities.append(abi)
						abi.upgrade()
					else: 
						dialogue(f'--- You have upgraded {abi}.\n')
						abi.upgrade()					
					self.abi_points -= 1
					return True

	def lvl_up(self):

		'''Whenever the player's xp reaches a certain point, they will level up'''

		clear()
		while self.xp >= (self.lvl + 2) ** 2:
			self.xp -= (self.lvl + 2) ** 2
			self.lvl += 1
			self.health += 50
			self.mana += 25
			self.current_health = self.health
			self.current_mana = self.mana
			self.abi_points += 1
			dialogue(f'--- You have leveled up to level {self.lvl}! Your power increases.\n')
			points = 3
			while points > 0:
				for stat in ['strength', 'intelligence', 'agility', 'defence']:
					current_stat = getattr(self, stat)
					upgrade = num_input(f'--- {stat.capitalize()}: {current_stat} ({points} points remaining) Add: ')
					if upgrade > points: upgrade = points
					points -= upgrade
					setattr(self, stat, current_stat + upgrade)
					clear()
					if points == 0:	
						break
			while self.abi_points > 0:
				if not self.learn_ability(): 
					break

	def save(self):

		'''Used to save player progress'''

		with open(f'{self.name}_player_data.txt', 'w') as file:
			file.write(encode(self))

	def combat(self, enemy):

		'''Used whenever the player enters combat'''

		self.status = {}

		enemy.current_health = enemy.health
		enemy.current_mana = enemy.mana
		enemy.status = {}

		dialogue(f'You encountered {enemy}!')
		your_turn = True
		while True:
			if your_turn:
				print(f'{self}\nHealth - {self.current_health}/{self.health}\nMana - {self.current_mana}/{self.mana}\n')
				print(f'{enemy}\nHealth - {enemy.current_health}/{enemy.health}\nMana - {enemy.current_mana}/{enemy.mana}\n')
				print('1) Attack')
				print('2) Abilities')
				print('3) Pass')
				choice = num_input()
				clear()
				if choice == 1:
					while True:
						print('Choose a target.')
						targets = [enemy]
						for i, char in enumerate(targets, 1):
							print(f'{i}) {char}')
						choice = num_input()
						clear()
						if choice > len(targets) or choice <= 0:
							print('--- Invalid choice')
							continue
						target = targets[choice - 1]
						break
					dialogue(f'You attack {target} with your weapon!')
					attack = self.attack(target)
					if attack.hit:
						dialogue(f'You hit {target} for {attack.damage} damage!')
						target.current_health -= attack.damage						
					else: 
						dialogue('You missed!')
				elif choice == 2: 
					back = False
					while True:
						print('Abilities')
						ability_list = [abi for abi in self.abilities if abi.active]
						for i, abi in enumerate(ability_list, 1):
							print(f'{i}) {abi} ({abi.cost} mana): {abi.desc}')
						print(f'{len(ability_list) + 1}) Back')
						choice = num_input()
						clear()
						if choice == len(ability_list) + 1:
							back = True
							break
						elif choice > len(ability_list) or choice <= 0:
							print('--- Invalid choice')
							continue
						ability = ability_list[choice - 1]
						if ability.cost > self.current_mana:
							print('--- Not enough mana')
							continue
						if ability.target == 'enemy' or ability.target == 'ally':
							while True:
								print('Choose a target.')
								if ability.target == 'enemy':
									targets = [enemy]
								else:
									targets = [self]
								for i, char in enumerate(targets, 1):
									print(f'{i}) {char}')
								choice = num_input()
								clear()
								if choice > len(targets) or choice <= 0:
									print('--- Invalid choice')
									continue
								target = targets[choice - 1]
								self, target = ability.use(self, target)
								self.current_mana -= ability.cost
								break
						elif ability.target == 'all_enemy':
							pass
						elif ability.target == 'all_ally':
							pass
						elif ability.target == 'all':
							pass
						break
					if back:
						continue
				elif choice == 3:
					dialogue('You passed.')
				else:
					print('--- Invalid choice')
					continue
				your_turn = False
			else:
				dialogue(f'{enemy} attacks!')
				attack = enemy.attack(self)
				if attack.hit:
					dialogue(f'{enemy} hit you for {attack.damage} damage!')
					self.current_health -= attack.damage
				else: 
					dialogue('It missed!')
				your_turn = True
			if enemy.current_health <= 0:
				win = True
				break
			if self.current_health <= 0:
				win = False
				break
		if win:
			dialogue(f'You defeated {enemy}, and gained {enemy.xp} xp and {enemy.gold} gold!')
			self.xp += enemy.xp
			self.gold += enemy.gold
		else:
			dialogue('You perished.')
		return win

class Class:

	def __init__(self, name, stat, weap):

		self.name = name
		self.stat = stat
		self.weap = weap

	def __repr__(self):

		return self.name

	def __str__(self):

		return self.name

class Item:
	
	def __init__(self, name, value = 0, amount = 0, quest = False):
		
		self.name = name
		self.value = value
		self.amount = amount
		self.quest = quest

	def find(self, char):

		'''Used whenever the player character recieves this item'''

		char.inventory.append(self)
		dialogue(f'--- You have recieved {self} worth {self.value} gold, and it has been added to your inventory.\n')
	
	def __repr__(self):

		return self.name

	def __str__(self):

		return self.name

class Weapon(Item):

	def __init__(self, name, damage, value = 0, amount = 0, quest = False):

		super().__init__(name, value, amount)
		self.damage = damage

class Ability:
	
	def __init__(self, name, desc, stat, cost, active, target):
		
		self.name = name
		self.desc = desc
		self.stat = stat
		self.cost = cost
		self.active = active
		self.target = target
		self.lvl = 0
		self.max_lvl = 3

	def __repr__(self):

		return self.name

	def __str__(self):

		return self.name

class Location:

	def __init__(self, name, visit_func):

		self.visit_func = visit_func
		self.name = name

	def visit(self, player):

		'''Used whenever the player visits the location'''

		dialogue(f'--- You travel to {self}.')
		self.visit_func(player)
	
	def __repr__(self):

		return self.name

	def __str__(self):

		return self.name

class Area(Location):

	def __init__(self, name, locations, safe):

		self.name = name
		self.locations = locations
		self.safe = safe

	def visit(self, player):

		'''Used whenever the player visits the area'''
		
		player.progress['area'] = self
		if self.safe:
			player.current_health = player.health
			player.current_mana = player.mana
		dialogue(f'--- You travel to {self}.')
		while True:
			print(self)
			for i, l in enumerate(self.locations, 1):
				print(f'{i}) {l}')
			print(f'{len(self.locations) + 1}) View Character')
			print(f'{len(self.locations) + 2}) Save')
			if player.xp >= (player.lvl + 2) ** 2:
				print(f'{len(self.locations) + 3}) Level up!')
			choice = num_input()
			if choice == len(self.locations) + 1: 
				player.view_stats()
				continue
			elif choice == len(self.locations) + 2: 
				player.save()
				clear()
				print('Saved successfully!')
				continue
			elif choice == len(self.locations) + 3 and player.xp >= (player.lvl + 2) ** 2: 
				player.lvl_up()
				continue
			elif choice > len(self.locations) or choice <= 0:
				clear()
				print('--- Invalid choice')
				continue
			clear()
			self.locations[choice - 1].visit(player)

class Shop(Location):

	def __init__(self, name, stock, greeting):

		self.name = name
		self.stock = stock
		self.greeting = greeting

	def visit(self, player):

		'''Used whenever the player visits the shop'''

		dialogue(f'--- You travel to {self}.')
		dialogue(self.greeting)
		while True:
			print(f'--- You have {player.gold} gold.')
			for i, item in enumerate(self.stock, 1):
				print(f'{i}) {item} - {item.value} gold')
			print(f'{len(self.stock) + 1}) Sell items')
			print(f'{len(self.stock) + 2}) Leave')
			choice = num_input()
			clear()
			if choice == len(self.stock) + 1:
				if player.inventory == []:
					print('--- error: inventory empty')
					continue
				while True:
					print(f'--- You have {player.gold} gold.')
					choice_inv = [i for i in player.inventory if not i.quest]
					for i, item in enumerate(choice_inv, 1):
						print(f'{i}) {item} - {int(item.value * 0.8)} gold')
					print(f'{len(choice_inv) + 1}) Back')
					choice = num_input()
					clear()
					if choice == len(choice_inv) + 1:
						break
					elif choice > len(choice_inv) or choice <= 0:
						print('--- Invalid choice')
						continue
					choice = choice_inv[choice - 1]
					player.gold += int(choice.value * 0.8)
					player.inventory.remove(choice)
					print(f'--- You sold a {choice} for {int(choice.value * 0.8)} gold.')
				continue
			elif choice == len(self.stock) + 2: 
				return
			elif choice > len(self.stock) or choice <= 0:
				print('--- Invalid choice')
				continue
			choice = self.stock[choice - 1]
			if choice.value > player.gold:
				print('--- Insufficient funds')
				continue
			player.gold -= choice.value
			player.inventory.append(choice)
			print(f'--- You bought a {choice} for {choice.value} gold.')

class Slime(Character):

	pass

'''
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
xp - how much xp gained when slain
gold - currency carried by the character
player character
class - determines what stat you favor; underdeveloped as of current
xp - Gain XP in battle; when you have enough, you will go up one level and you will get to use your skill points.
abi_points - If the player cannot learn abilities at the moment, they will recieve an ability point to use for later.
'''

king_story = (
	'Very well. Go ahead and take a seat.',
	'Now, Asathryne once was a kingdom filled with happiness and peace, ruled by Emperor Verandus.',
	'Until one day, an evil never before seen, arrived in Asathryne and tore the realm apart, leaving nothing but a barren wasteland.',
	'Sanctuary became the only thriving town left in the land.',
	'The horrid evil killed the emperor and kidnapped his daughter, our future princess. She was one of the most powerful beings in Asathryne.',
	'But this was twenty years ago. Much longer ago, when we had a fighting chance against the dark forces.',
	'We have long waited for a courageous adventurer who would be worthy enough to venture into the depths of Asathryne and rescue us from this terror.')
'''
Basically, here's how it goes:
Princess is born to emperor, and they find out she's super magical and has immense powers.
Emperor goes into deep cave. Or something. Or maybe some servant or adventerer goes. He discovers a book or something. The book contains dark magics.
The emperor reads the book and becomes corrupted with the dark magics. He hears voices telling him to summon a bunch of dark creatures.
He uses princess as a conduit to summon the army, fakes his own death, and travels to a mountain where nobody can find his daughter.
Continues summoning army until they destroy asathryne.
'''

axe = Weapon('Axe', (25, 50), 10)
staff = Weapon('Staff', (25, 30), 10)
bow = Weapon('Bow', (30, 35), 10)
sword = Weapon('Sword', (35, 40), 10)
sanctuary_key = Item('Sanctuary Key', quest = True)
pot_health = Item('Health Potion', 20)
pot_mana = Item('Mana Potion', 20)

warrior = Class('Warrior', 'strength', axe)
sorcerer = Class('Sorcerer', 'intelligence', staff)
ranger = Class('Ranger', 'agility', bow)
paladin = Class('Paladin', 'defence', sword)
classes = [warrior, sorcerer, ranger, paladin]

sanctuary_apothecary = Shop(
	name = 'Sanctuary Apothecary',
	stock = [pot_health, pot_mana],
	greeting = 'Welcome to the Apothecary! We have a variety of potions for sale. Take a look at what we have in stock.')
sanctuary_blacksmith = Shop(
	name = 'Sanctuary Blacksmith',
	stock = [axe, staff, bow, sword],
	greeting = 'Hello there, traveller! You look like you could use a reliable weapon. Step into my shop and take a look at my many wares!')

def sanctuary_gates_visit(player):
	if player.progress['gates_unlocked']:
		forest_of_mysteries.visit(player)
		return
	elif player.progress['king_dialogue']:
		dialogue('Asathryne Gatekeeper: Halt there, young - ')
		dialogue('Oh. You spoke with the King? I suppose my orders are to let you through then. Here, hand me the key.')
		while True:
			last_option = dialogue('1) Return to Sanctuary\n2) Unlock the gates\n')
			if last_option == '1':
				dialogue('Very well. Return to the town square, and come back here when you are ready.')
				return
			elif last_option == '2':
				player.item_remove(sanctuary_key)
				dialogue('--- You give the key to the gatekeeper. The gates open, revealing an expansive forest, teeming with otherworldly life.')
				dialogue('Good luck out there, traveller.')
				player.progress['gates_unlocked'] = True
				forest_of_mysteries.visit(player)
				return
			else: 
				print('--- Invalid choice')
	dialogue('Asathryne Gatekeeper: Halt there, young traveller! There is a dangerous, dark evil behind these gates. I shall not let you pass, unless you have spoken with the King of Asathryne!')
	player.progress['gates_dialogue'] = True
	while True:
		option_gate = dialogue('Type \'go\' to go meet King Brand, or \'exit\' to return to the town square.\n').lower()
		if option_gate == 'go':
			sanctuary_kings_palace.visit(player)
			return
		elif option_gate == 'exit':
			clear()
			dialogue('--- You return to the town square.')
			return
		else:
			clear()
			gate_random = randint(1, 3)
			if gate_random == 1: 
				dialogue('What are you waiting for? Go on!')
			elif gate_random == 2: 
				dialogue('Don\'t think standing here will convince me to open this gate.')
			else: 
				dialogue('Brand is waiting for you.')
sanctuary_gates = Location('Sanctuary Gates', sanctuary_gates_visit)

def sanctuary_kings_palace_visit(player):
	if player.progress['king_dialogue']:
		dialogue('King Brand: Hello, young traveller.')
		while True:
			king_story_repeat = dialogue('Do you wish to hear the story of Asathryne? (Y/N): ').lower()
			if king_story_repeat == 'y':
				for s in king_story: dialogue(s)
				return
			elif king_story_repeat == 'n':
				dialogue('Oh well, maybe for another day. Fare well, traveller!')
				return
			else:
				print('--- Invalid choice')
	dialogue(f'King Brand: At last, a brave {player.class_type} has arisen once more in this kingdom, here on a quest to save the kingdom of Asathryne from the dark evil that lies beyond the gates.')
	dialogue('Tell me young traveller, what do you seek from me?')
	while True:
		if player.progress['gates_dialogue']: 
			option_1 = dialogue('1) I\'m here to learn about Asathryne\n2) The gate keeper has sent me to meet you\n')
		else: 
			option_1 = dialogue('1) I\'m here to learn about Asathryne\n')
		if option_1 == '1':
			for s in king_story: 
				dialogue(s)
			dialogue('You will be the one to free us from this crisis.')
			dialogue('Here, take this key; you will need it to open the gate into what remains of Asathryne.')
			sanctuary_key.find(player)
			dialogue('Fare well, young traveller.')
			player.progress['king_dialogue'] = True
			return
		elif option_1 == '2' and player.progress['gates_dialogue']:
			dialogue('Ah, the gate keeper. He forbids anyone entry to the rest of Asathryne, simply because he wants to protect them.')
			break
		else:
			print('--- Invalid choice')
	while True:
		option_2 = dialogue('Let me ask you a question, traveller. Would you like to hear the Story of Asathryne? (Y/N)\n').lower()
		if option_2 == 'n':
			dialogue('Very well, very well, let me see... it\'s here somewhere... ah! The Key to Asathryne. Take this, young traveller, and good luck!')
			sanctuary_key.find(player)
			player.progress['king_dialogue'] = True
			return
		elif option_2 == 'y':
			for s in king_story:
				dialogue(s)
			dialogue('You will be the one to free us from this crisis.')
			dialogue('Here, take this key; you will need it to open the gate into what remains of Asathryne.')
			sanctuary_key.find(player)
			dialogue('Fare well, young traveller.')
			player.progress['king_dialogue'] = True
			return
		else:
			print('--- Invalid choice')
sanctuary_kings_palace = Location('Sanctuary King\'s Palace', sanctuary_kings_palace_visit)

def forest_main_visit(player):
	player.combat(Slime(
		name = 'Green Slime',
		health = 50,
		mana = 0,
		lvl = 1,
		strength = 3,
		intelligence = 0,
		agility = 4,
		defence = 2,
		weap = Weapon('Slime', (30, 40)),
		gold = randint(3, 6),
		xp = randint(2, 3)))
forest_main = Location('Forest Main', forest_main_visit)

sanctuary = Area('Sanctuary', (sanctuary_gates, sanctuary_kings_palace, sanctuary_apothecary, sanctuary_blacksmith), True)
forest_of_mysteries = Area('Forest of Mysteries', (sanctuary, forest_main), False)

class Stun(Ability):

	def __init__(self):
		
		super().__init__(
			name = 'Stun',
			desc = 'You swing your weapon, stunning target enemy for a duration.',
			stat = 'strength',
			cost = 40,
			active = True,
			target = 'enemy')
		
	def upgrade(self):

		'''Levels up this ability, increasing its level and other stats'''

		self.lvl += 1
		self.damage = {1: 1.2, 2: 1.4, 3: 1.5}.get(self.lvl)
		self.duration = {1: 1, 2: 1, 3: 2}.get(self.lvl)

	def check(self, user):

		'''Checks if player is eligible to learn/upgrade this ability'''

		if getattr(user, self.stat) >= {0: 8, 1: 13, 2: 20}.get(self.lvl):
			return True
		return False

	def use(self, user, target):

		dialogue(f'{user} uses {self} on {target}!')
		attack = user.attack(target, damage_multiplier = self.damage, accuracy_multiplier = 0.9)
		if attack.hit:
			dialogue(f'{user} deals {attack.damage} damage and stuns {target} for {self.duration} turn!')
			target.current_health -= attack.damage
			target.status['stun'] = self.duration
		else:
			dialogue(f'{user} missed!')
		return (user, target)

class Fireball(Ability):

	def __init__(self):
		
		super().__init__(
			name = 'Fireball',
			desc = 'You hurl a fireball at target enemy, dealing damage.',
			stat = 'intelligence',
			cost = 10,
			active = True,
			target = 'enemy')

	def upgrade(self):

		'''Levels up this ability, increasing its level and other stats'''

		self.lvl += 1
		self.damage = {1: 4, 2: 7, 3: 10}.get(self.lvl)

	def check(self, user):

		'''Checks if player is eligible to learn/upgrade this ability'''

		if getattr(user, self.stat) >= {0: 8, 1: 13, 2: 20}.get(self.lvl):
			return True
		return False

	def use(self, user, target):

		dialogue(f'{user} uses {self} on {target}!')
		damage = self.damage * user.intelligence
		dialogue(f'The fireball burns {target} dealing {damage} damage!')
		target.current_health -= damage
		return (user, target)

class SureShot(Ability):

	def __init__(self):
		
		super().__init__(
			name = 'Sure Shot',
			desc = 'You fire a well-aimed shot from your bow at target enemy, more damaging and accurate than a normal attack.',
			stat = 'agility',
			cost = 15,
			active = True,
			target = 'enemy')
		
	def upgrade(self):

		'''Levels up this ability, increasing its level and other stats'''

		self.lvl += 1
		self.damage = {1: 1.3, 2: 1.5, 3: 1.7}.get(self.lvl)
		self.accuracy = {1: 1.5, 2: 1.5, 3: 2}.get(self.lvl)

	def check(self, user):

		'''Checks if player is eligible to learn/upgrade this ability'''

		if getattr(user, self.stat) >= {0: 8, 1: 13, 2: 20}.get(self.lvl):
			return True
		return False

	def use(self, user, target):

		dialogue(f'{user} uses {self} on {target}!')
		attack = user.attack(target, damage_multiplier = self.damage, accuracy_multiplier = self.accuracy)
		if attack.hit:
			dialogue(f'{user} deals {attack.damage} damage to {target}!')
			target.current_health -= attack.damage
		else:
			dialogue(f'{user} missed!')
		return (user, target)

class Protection(Ability):

	def __init__(self):
		
		super().__init__(
			name = 'Protection',
			desc = 'You summon a magical wall of protection, which prevents a percentage of damage dealt to target ally for a duration.',
			stat = 'defence',
			cost = 30,
			active = True,
			target = 'ally')

	def upgrade(self):

		'''Levels up this ability, increasing its level and other stats'''

		self.lvl += 1
		self.resistance = {1: 1.3, 2: 1.5, 3: 1.6}.get(self.lvl)
		self.duration = {1: 2, 2: 2, 3: 3}.get(self.lvl)

	def check(self, user):

		'''Checks if player is eligible to learn/upgrade this ability'''

		if getattr(user, self.stat) >= {0: 8, 1: 13, 2: 20}.get(self.lvl):
			return True
		return False

	def use(self, user, target):

		dialogue(f'{user} uses {self} on {target}!')
		target.status['resistance'] = [self.resistance, self.duration]
		dialogue(f'{target}\'s resistance has been increased for {self.duration} turns!')
		return (user, target)

abilities = [Stun(), Fireball(), SureShot(), Protection()]

def main():
	clear()
	while True:
		print(f'>>> Asathryne <<< v{version}')
		print('1) New game\n2) Load game')
		choice = num_input()
		clear()
		if choice == 1:
			dialogue('Before the game begins, I want to thank you for playing this beta version of the game!')
			dialogue('The reason I\'m probably having you play this is because I really need help with developing this game.')
			dialogue('All I ask of you is to provide any and all feedback and suggestions that you have for me.')
			dialogue('If possible, I\'m also looking for people who are good at creative writing and worldbuilding to help me develop story!')
			print('One more thing, here are a couple known bugs in this version. If you run into something not on this list, please report it.')
			for bug in bugs:
				print(f' - {bug}')
			dialogue()
			dialogue('Thanks so much, and I hope you enjoy!')
			player = PlayerCharacter()
			player.build_char()
			if dialogue('--- Type \'skip\' to skip the tutorial, or press enter to continue\n') == 'skip':
				player.equip(player.class_type.weap)
				player.lvl_up()
			else:
				dialogue(f'Welcome to The Realm of Asathryne, {player}. A kingdom filled with adventure and danger, with much in store for those brave enough to explore it. Of course, nothing a {player.class_type} such as yourself can\'t handle.')
				dialogue('Oh, of course! Allow me to introduce myself. My name is Kanron, your advisor.')
				dialogue(f'You can\'t just go wandering off into Asathryne without a weapon. Every {player.class_type} needs a {player.class_type.weap}!')
				player.equip(player.class_type.weap)
				dialogue('Before you go venturing off into the depths of this realm, you must first master some basic skills.')
				dialogue('Your stats determine your performance in battle, and the abilities you can learn.')
				dialogue('There are 4 main stats: Strength, Intelligence, Agility, and Defense.')
				while True:
					learn_more = dialogue('Do you want to learn more about stats? (Y/N)\n').lower()
					if learn_more == 'y':
						dialogue('Strength increases the amount of damage you deal with physical attacks.')
						dialogue('Intelligence increases the potency of your spells.')
						dialogue('Agility determines the accuracy of your attacks, and how often you dodge attacks.')
						dialogue('Defense determines how much damage you take from physical attacks.')
						dialogue('Your mana determines your use of abilities.')
						dialogue('Your health determines how much damage you can take before you perish.')
						break
					elif learn_more == 'n': 
						break
					else: 
						print('--- Invalid choice')
				dialogue('Let\'s talk about your level.')
				dialogue('Your level represents how powerful you are, and determines the level of your enemies; when you go up a level, you will recieve 3 skill points to spend on any of the 4 stats, and 1 ability point to learn/upgrade abilities. Additionally, your health and mana will automatically increase.')
				dialogue('You can gain XP (experience points) in battle; when you have enough, you\'ll go up one level and get to use your skill points.')
				dialogue('Let\'s upgrade your stats. For your class, you recieve an extra 3 skill points in the stat that your class favors, and you will recieve 1 level up.')
				player.lvl_up()
				dialogue('Great job! Now that you have learned the basics, it is time you start your journey into the Realm of Asathryne.')
			sanctuary.visit(player)
		elif choice == 2:
			saves = []
			for file in os.listdir(os.fsencode(os.getcwd())):
				filename = os.fsdecode(file)
				if 'player_data' in filename: 
					with open(filename, 'r') as file:
						saves.append(decode(file.read()))
			if saves == []:
				print('No saves found')
				continue
			while True:
				print('Choose your character.')
				for i, s in enumerate(saves, 1):
					print(f'{i}) {s.name} - Level {s.lvl} {s.class_type}')
				choice = num_input()
				clear()
				if choice <= 0 or choice > len(saves):
					print('--- Invalid choice')
					continue
				player = saves[choice - 1] 
				player.progress['area'].visit(player)
		else:
			print('--- Invalid choice')
if __name__ == '__main__': 
	main()
