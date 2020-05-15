from random import randint
import simplejson
import os
import time
import keyboard
from jsonpickle import encode, decode
from stuff import clear, dialogue, num_input, choose, clear_input, delay

__version__ = '0.2.5'

'''
Roadmap

now:
0.3.1
rework items
	- active items
	- equipping items
	- equipment dict attribute
	- item requirements to equip
rework view character
	- choose from 3 sections
	- stats, abilities, items sections
	- stats - display info about current stats
	- abilities - list known abilities, what they do, cost, etc
	- items - currently equipped items, empty slots, inventory, equip items

soon:
clean up keyboard usage
	- should have no effect on typing outside of the application
	- on_press/on_release?
	- input lag and eccessive enter handling
debug mode
	- commands for debugging
followers/allies
	- followers list attribute
	- controllable/ai
expand classes
	- subclasses
expand combat
	- enemy abilities/items
	- combat stat balancing
	- enemy ai
	- allies
	- status effects
abilities 
	- global targeting
	- passives and actives
quests
	- quest board
	- npcs
map/locations
	- grid

later:
backwards compatibility
pygame
guis
multiplayer
	- pvp
	- co-op
'''

class Character():
	
	def __init__(self, name, health, mana, lvl, stats, xp, gold, weap, abilities = [], inventory = []):

		self.name = name 
		self.health = health
		self.mana = mana
		self.lvl = lvl
		self.stats = stats
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
		print(f'Strength - {self.stats["strength"]}')
		print(f'Intelligence - {self.stats["intelligence"]}')
		print(f'Agility - {self.stats["agility"]}')
		print(f'Defence - {self.stats["defence"]}')
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

		if randint(1, 100) < (self.stats['agility'] / (self.stats['agility'] + target.stats['agility'])) * 100 * accuracy_multiplier:
			hit = True
			damage = int(self.stats['strength'] / (self.stats['strength'] + target.stats['defence']) * randint(*self.weap.damage) * damage_multiplier)
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

		super().__init__(name = '', health = 50, mana = 25, lvl = 0, stats = {'strength': 5, 'intelligence': 5, 'agility': 5, 'defence': 5}, xp = 4, gold = 50, weap = '')
		self.progress = {'area': '', 'king_dialogue': False, 'gates_dialogue': False, 'gates_unlocked': False}
		self.class_type = ''
		self.abi_points = 0
		self.version = __version__

	def view_stats(self):

		'''Used to display data about the player character to the player'''

		clear()
		print(self)
		print(f'Level {self.lvl} {self.class_type}')
		print(f'{self.gold} Gold')
		print(f'{self.xp}/{(self.lvl + 2) ** 2} xp')
		print(f'{self.abi_points} ability points')
		print(f'{self.current_health}/{self.health} health')
		print(f'{self.current_mana}/{self.mana} mana')
		print(f'Strength - {self.stats["strength"]}')
		print(f'Intelligence - {self.stats["intelligence"]}')
		print(f'Agility - {self.stats["agility"]}')
		print(f'Defence - {self.stats["defence"]}')
		print(f'Weapon - {self.weap} ({self.weap.damage[0]}-{self.weap.damage[1]} damage)')
		print(f'Abilities - {self.abilities}')
		print(f'Inventory - {self.inventory}')
		dialogue()

	def build_char(self):

		'''Used in the beginning to build the player character'''

		self.name = ''
		while self.name == '':
			self.name = clear_input('What is your name, traveller?\n')
			if self.name == '': 
				print('You must have have a name in this realm.')
		self.class_type = classes[choose('Choose a class.', classes) - 1]
		dialogue(f'--- You chose the {self.class_type} class, which favors {self.class_type.stat}.')
		self.stats[self.class_type.stat] += 3
		self.inventory.append(self.class_type.weap)

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
			dialogue(f'--- {item} has been removed from your inventory.')
			self.inventory.remove(item)
			return True
		return False

	def learn_ability(self, abilities):

		'''Used whenever the player character can learn a new ability; only used in lvl_up as of current'''

		ability_list = [abi for abi in self.abilities if abi.max_lvl > abi.lvl and abi.check(self)]
		for abi in abilities: 
			if abi.check(self):
				if all(a.name != abi.name for a in self.abilities):
					ability_list.append(abi)
		if ability_list == []:
			dialogue('--- There are no avaliable abilities to learn/upgrade.')
			return False
		abi_info = [f'{abi} ({abi.lvl}/{abi.max_lvl}): {abi.desc}' for abi in ability_list]
		ability = ability_list[choose(f'--- You have {len(ability_list)} abilities to learn/upgrade.', abi_info) - 1]
		if ability.lvl == 0: 
			dialogue(f'--- You have learned {ability}.')
			self.abilities.append(ability)
		else: 
			dialogue(f'--- You have upgraded {ability}.')
		ability.upgrade()
		self.abi_points -= 1
		return True

	def lvl_up_threshold(self):

		return (self.lvl + 2) ** 2

	def lvl_up_avaliable(self):

		return self.xp >= self.lvl_up_threshold()

	def lvl_up(self, abilities):

		'''Whenever the player's xp reaches a certain point, they will level up'''

		clear()
		if not self.lvl_up_avaliable():
			print('--- Unable to level up')
			return
		while self.lvl_up_avaliable():
			self.xp -= self.lvl_up_threshold()
			self.lvl += 1
			self.health += 50
			self.mana += 25
			self.current_health = self.health
			self.current_mana = self.mana
			self.abi_points += 1
			dialogue(f'--- You have leveled up to level {self.lvl}! Your power increases.\n')
			points = 3
			choice = 1
			choices = ['Strength', 'Intelligence', 'Agility', 'Defence']
			while points > 0:
				print(f'You have {points} points.')
				for i, c in enumerate(choices, 1):
					print(f' {">" if i == choice else "-"} {c}: {self.stats[c.lower()]}')
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
					self.stats[choices[choice - 1].lower()] += 1
					clear()
					points -= 1
				clear()
			while self.abi_points > 0:
				if not self.learn_ability(abilities): 
					break

	def save(self):

		'''Used to save player progress'''

		with open(f'{self.name}_player_data.txt', 'w') as file:
			file.write(encode(self))
		clear()
		print('--- Saved successfully!')

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
				self_info = f'{self}\nHealth - {self.current_health}/{self.health}\nMana - {self.current_mana}/{self.mana}\n'
				enemy_info = f'{enemy}\nHealth - {enemy.current_health}/{enemy.health}\nMana - {enemy.current_mana}/{enemy.mana}\n'
				choice = choose(f'{self_info}\n{enemy_info}', ('Attack', 'Abilities', 'Pass'))
				if choice == 1:
					targets = [enemy]
					target = targets[choose('Choose a target.', targets) - 1]
					dialogue(f'You attack {target} with your weapon!')
					attack = self.attack(target)
					if attack.hit:
						dialogue(f'You hit {target} for {attack.damage} damage!')
						target.current_health -= attack.damage
					else: 
						dialogue('You missed!')
				elif choice == 2: 
					choices = [abi for abi in self.abilities if abi.active] + ['Back']
					choice_info = [f'{c} ({c.cost} mana): {c.desc}' if type(c) != str else c for c in choices]
					while True:
						choice = choices[choose('Abilities', choice_info) - 1]
						if type(choice) != str:
							if choice.cost > self.current_mana:
								print('--- Not enough mana')
								continue
						break
					if choice == 'Back':
						continue
					elif choice.target == 'enemy' or choice.target == 'ally':
						if choice.target == 'enemy':
							targets = [enemy]
						else:
							targets = [self]
						target = targets[choose('Choose a target.', targets) - 1]
						choice.use(self, target)
						self.current_mana -= choice.cost
					elif choice.target == 'all_enemy':
						pass
					elif choice.target == 'all_ally':
						pass
					elif choice.target == 'all':
						pass
				elif choice == 3:
					dialogue('You passed.')
				your_turn = False
			else:
				dialogue(f'{enemy} attacks!')
				attack = enemy.attack(self)
				if attack.hit:
					dialogue(f'{enemy} hit {self} for {attack.damage} damage!')
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

	def find(self, player):

		'''Used whenever the player character recieves this item'''

		player.inventory.append(self)
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
	
	def __init__(self, name, desc, cost, active, target):
		
		self.name = name
		self.desc = desc
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
			choices = self.locations + ('View Character', 'Save') + (('Level up!',) if player.lvl_up_avaliable() else ())
			choice = choices[choose(self, choices) - 1]
			if choice == 'View Character': 
				player.view_stats()
			elif choice == 'Save': 
				player.save()
			elif choice == 'Level up!': 
				player.lvl_up(abilities)
			else:
				choice.visit(player)

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
			choices = self.stock + ('Sell items', 'Leave')
			choice_info = [f'{c} - {c.value} gold' if type(c) != str else c for c in choices]
			choice = choices[choose(f'--- You have {player.gold} gold.', choice_info) - 1]
			if type(choice) != str:
				if choice.value > player.gold:
					print('--- Insufficient funds')
					continue
			if choice == 'Sell items':
				while True:
					choices = [i for i in player.inventory if not i.quest] + ['Back']
					choice_info = [f'{c} - {int(c.value * 0.8)} gold' if type(c) != str else c for c in choices]
					if choices == ['Back']:
						print('--- Nothing to sell')
						break
					choice = choices[choose(f'--- You have {player.gold} gold.', choice_info) - 1]
					if choice == 'Back':
						break
					else:
						player.gold += int(choice.value * 0.8)
						player.inventory.remove(choice)
						print(f'--- You sold a {choice} for {int(choice.value * 0.8)} gold.')
			elif choice == 'Leave': 
				return
			else:
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
	stock = (pot_health, pot_mana),
	greeting = 'Apothecary: Welcome to the Apothecary! We have a variety of potions for sale. Take a look at what we have in stock.')
sanctuary_blacksmith = Shop(
	name = 'Sanctuary Blacksmith',
	stock = (axe, staff, bow, sword),
	greeting = 'Blacksmith: Hello there, traveller! You look like you could use a reliable weapon. Step into my shop and take a look at my many wares!')

def sanctuary_gates_visit(player):
	if player.progress['gates_unlocked']:
		forest_of_mysteries.visit(player)
		return
	elif player.progress['king_dialogue']:
		dialogue('Asathryne Gatekeeper: Halt there, young - ')
		choice = choose(
			'Asathryne Gatekeeper: Oh. You spoke with the King? I suppose my orders are to let you through then. Here, hand me the key.',
			('Return to Sanctuary', 'Unlock the gates'))
		if choice == 1:
			dialogue('Asathryne Gatekeeper: Very well. Return to the town square, and come back here when you are ready.')
			dialogue('--- You return to the town square.')
			return
		else:
			player.item_remove(sanctuary_key)
			dialogue('--- You give the key to the gatekeeper. The gates open, revealing an expansive forest, teeming with otherworldly life.')
			dialogue('Asathryne Gatekeeper: Good luck out there, traveller.')
			player.progress['gates_unlocked'] = True
			forest_of_mysteries.visit(player)
			return
	choice = choose(
		'Asathryne Gatekeeper: Halt there, young traveller! There is a dangerous, dark evil behind these gates. I shall not let you pass, unless you have spoken with the King of Asathryne!',
		('Meet the king', 'Return to town square'))
	player.progress['gates_dialogue'] = True
	if choice == 1:
		sanctuary_kings_palace.visit(player)
		return
	else:
		clear()
		dialogue('--- You return to the town square.')
		return
sanctuary_gates = Location('Sanctuary Gates', sanctuary_gates_visit)

def sanctuary_kings_palace_visit(player):
	if player.progress['king_dialogue']:
		dialogue('King Brand: Hello, young traveller.')
		choice = choose('King Brand: Do you wish to hear the story of Asathryne?', ('Yes', 'No'))
		if choice == 1:
			dialogue('King Brand: Very well. Go ahead and have a seat.')
			for line in king_story: 
				dialogue(f'King Brand: {line}')
			return
		else:
			dialogue('King Brand: Oh well, maybe for another day. Fare well, traveller!')
			return
	dialogue(f'King Brand: At last, a brave {player.class_type} has arisen once more, here on a quest to save the kingdom of Asathryne from the dark evil that lies beyond the gates.')
	if player.progress['gates_dialogue']: 
		choice = choose(
			'King Brand: Tell me young traveller, what do you seek from me?',
			('I\'m here to learn about Asathryne', 'The gate keeper has sent me to meet you'))
	else: 
		choice = choose(
			'King Brand: Tell me young traveller, what do you seek from me?',
			('I\'m here to learn about Asathryne',))
	if choice == 1:
		dialogue('King Brand: Very well. Go ahead and have a seat.')
		for line in king_story: 
			dialogue(f'King Brand: {line}')
		dialogue('King Brand: You will be the one to free us from this crisis.')
		dialogue('King Brand: Here, take this key; you will need it to open the gate into what remains of Asathryne.')
		sanctuary_key.find(player)
		dialogue('King Brand: Fare well, young traveller.')
		player.progress['king_dialogue'] = True
		return
	else:
		dialogue('King Brand: Ah, the gate keeper. He forbids anyone entry to the rest of Asathryne, simply because he wants to protect them.')
	choice = choose(
		'King Brand: Let me ask you a question, traveller. Would you like to hear the Story of Asathryne?',
		('Yes', 'No'))
	if choice == 1:
		dialogue('King Brand: Very well. Go ahead and have a seat.')
	else:
		dialogue('King Brand: Nonsense, I must regale this lore, it is my duty!')
	for line in king_story: 
		dialogue(f'King Brand: {line}')
	dialogue('King Brand: You will be the one to free us from this crisis.')
	dialogue('King Brand: Here, take this key; you will need it to open the gate into what remains of Asathryne.')
	sanctuary_key.find(player)
	dialogue('King Brand: Fare well, young traveller.')
	player.progress['king_dialogue'] = True
	return
sanctuary_kings_palace = Location('Sanctuary King\'s Palace', sanctuary_kings_palace_visit)

def forest_visit(player):
	player.combat(Slime(
		name = 'Green Slime',
		health = 50,
		mana = 0,
		lvl = 1,
		stats = {'strength': 3,
		'intelligence': 0,
		'agility': 4,
		'defence': 2},
		weap = Weapon('Slime', (30, 40)),
		gold = randint(3, 6),
		xp = randint(2, 3)))
forest = Location('Forest', forest_visit)

sanctuary = Area('Sanctuary', (sanctuary_gates, sanctuary_kings_palace, sanctuary_apothecary, sanctuary_blacksmith), True)
forest_of_mysteries = Area('Forest of Mysteries', (sanctuary, forest), False)

class Stun(Ability):

	def __init__(self):
		
		super().__init__(
			name = 'Stun',
			desc = 'You attack with immense force, stunning target enemy for a duration.',
			cost = 40,
			active = True,
			target = 'enemy')
		
	def upgrade(self):

		'''Levels up this ability, increasing its level and other stats'''

		self.lvl += 1
		self.damage = {1: 1.2, 2: 1.4, 3: 1.5}[self.lvl]
		self.duration = 1

	def check(self, user):

		'''Checks if player is eligible to learn/upgrade this ability'''

		return user.stats['strength'] >= {0: 8, 1: 13, 2: 20}[self.lvl]

	def use(self, user, target):

		dialogue(f'{user} uses {self} on {target}!')
		attack = user.attack(target, damage_multiplier = self.damage, accuracy_multiplier = 0.9)
		if attack.hit:
			dialogue(f'{user} deals {attack.damage} damage and stuns {target} for {self.duration} turn!')
			target.current_health -= attack.damage
			target.status['stun'] = self.duration
		else:
			dialogue(f'{user} missed!')

class Fireball(Ability):

	def __init__(self):
		
		super().__init__(
			name = 'Fireball',
			desc = 'You hurl a fireball at target enemy, dealing damage.',
			cost = 10,
			active = True,
			target = 'enemy')

	def upgrade(self):

		'''Levels up this ability, increasing its level and other stats'''

		self.lvl += 1
		self.damage = {1: 4, 2: 7, 3: 10}[self.lvl]

	def check(self, user):

		'''Checks if player is eligible to learn/upgrade this ability'''

		return user.stats['intelligence'] >= {0: 8, 1: 13, 2: 20}[self.lvl]

	def use(self, user, target):

		dialogue(f'{user} uses {self} on {target}!')
		damage = int(self.damage * user.stats['intelligence'] * (randint(90, 110) / 100))
		dialogue(f'The fireball burns {target} dealing {damage} damage!')
		target.current_health -= damage
		#return (user, target)

class SureStrike(Ability):

	def __init__(self):
		
		super().__init__(
			name = 'Sure Strike',
			desc = 'You precisely attack target enemy, more damaging and accurate than a normal attack.',
			cost = 15,
			active = True,
			target = 'enemy')
		
	def upgrade(self):

		'''Levels up this ability, increasing its level and other stats'''

		self.lvl += 1
		self.damage = {1: 1.3, 2: 1.5, 3: 1.7}[self.lvl]
		self.accuracy = {1: 1.5, 2: 1.5, 3: 2}[self.lvl]

	def check(self, user):

		'''Checks if player is eligible to learn/upgrade this ability'''

		return user.stats['agility'] >= {0: 8, 1: 13, 2: 20}[self.lvl]

	def use(self, user, target):

		dialogue(f'{user} uses {self} on {target}!')
		attack = user.attack(target, damage_multiplier = self.damage, accuracy_multiplier = self.accuracy)
		if attack.hit:
			dialogue(f'{user} deals {attack.damage} damage to {target}!')
			target.current_health -= attack.damage
		else:
			dialogue(f'{user} missed!')

class Protection(Ability):

	def __init__(self):
		
		super().__init__(
			name = 'Protection',
			desc = 'You summon a magical wall of protection, which prevents a percentage of damage dealt to target ally for a duration.',
			cost = 30,
			active = True,
			target = 'ally')

	def upgrade(self):

		'''Levels up this ability, increasing its level and other stats'''

		self.lvl += 1
		self.resistance = {1: 1.3, 2: 1.5, 3: 1.6}[self.lvl]
		self.duration = {1: 2, 2: 2, 3: 3}[self.lvl]

	def check(self, user):

		'''Checks if player is eligible to learn/upgrade this ability'''

		return user.stats['defence'] >= {0: 8, 1: 13, 2: 20}[self.lvl]

	def use(self, user, target):

		dialogue(f'{user} uses {self} on {target}!')
		target.status['resistance'] = [self.resistance, self.duration]
		dialogue(f'{target}\'s resistance has been increased for {self.duration} turns!')

abilities = [Stun(), Fireball(), SureStrike(), Protection()]

def main():
	clear()
	while True:
		choice = choose(f'>>> Asathryne <<< v{__version__}\n(Use arrow keys and press enter to select)', ('New game', 'Load game', 'Help'))
		if choice == 1:
			player = PlayerCharacter()
			player.build_char()
			if choose('Skip the tutorial?', ('Yes', 'No')) == 1:
				player.equip(player.class_type.weap)
				player.lvl_up(abilities)
			else:
				dialogue(f'Welcome to The Realm of Asathryne, {player}. A kingdom filled with adventure and danger, with much in store for those brave enough to explore it. Of course, nothing a {player.class_type} such as yourself can\'t handle.')
				dialogue('Oh, of course! Allow me to introduce myself. My name is Kanron, your advisor.')
				dialogue(f'Kanron: You can\'t just go wandering off into Asathryne without a weapon. Every {player.class_type} needs a {player.class_type.weap}!')
				player.equip(player.class_type.weap)
				dialogue('Kanron: Before you go venturing off into the depths of this realm, you must first master some basic skills.')
				dialogue('Kanron: Your stats determine your performance in battle, and the abilities you can learn.')
				dialogue('Kanron: There are 4 main stats: Strength, Intelligence, Agility, and Defense.')
				choice = choose('Kanron: Do you want to learn more about stats?', ('Yes', 'No'))
				if choice == 1:
					while True:
						dialogue('Kanron: Strength increases the amount of damage you deal with physical attacks.')
						dialogue('Kanron: Intelligence increases the potency of your spells.')
						dialogue('Kanron: Agility determines the accuracy of your attacks, and how often you dodge attacks.')
						dialogue('Kanron: Defense determines how much damage you take from physical attacks.')
						dialogue('Kanron: Your mana determines your use of abilities.')
						dialogue('Kanron: Your health determines how much damage you can take before you perish.')
						if choose('Kanron: Would you like me to repeat stats?', ('Yes', 'No')) == 2:
							break
				dialogue('Kanron: Let\'s talk about your level.')
				dialogue('Kanron: Your level represents how powerful you are, and determines the level of your enemies; when you go up a level, you will recieve 3 skill points to spend on any of the 4 stats, and 1 ability point to learn/upgrade abilities. Additionally, your health and mana will automatically increase and regenerate.')
				dialogue('Kanron: You can gain XP (experience points) in battle; when you have enough, you\'ll go up one level and get to use your skill points.')
				dialogue('Kanron: Let\'s upgrade your stats. For your class, you recieve an extra 3 skill points in the stat that your class favors, and you will recieve 1 level up.')
				player.lvl_up(abilities)
				dialogue('Kanron: Great job! Now that you have learned the basics, it is time you start your journey into the Realm of Asathryne.')
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
			saves_info = [f'{c.name} - Level {c.lvl} {c.class_type}' for c in saves]
			player = saves[choose('Choose your character.', saves_info) - 1] 
			try:
				if player.version != __version__:
					dialogue(f'WARNING: This character was created in version {player.version}. Current version is {__version__}. If you continue, unexpected errors may occur.')
			except AttributeError:
				dialogue(f'WARNING: This character was created in an older version. Current version is {__version__}. If you continue, unexpected errors may occur.')
			player.progress['area'].visit(player)
		elif choice == 3:
			dialogue('To select options in any menu, use the up and down arrow keys to select the desired option and press enter.')
if __name__ == '__main__': 
	main()
