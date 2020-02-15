from requests import get
from stuff import *

class Item:

	def __init__(self, name, price, spell_1, spell_2):

		self.name = name
		self.price = price
		self.spell_1 = spell_1
		self.spell_2 = spell_2

	def __str__(self):

		text = f'Name - {self.name}\nPrice - {self.price}\nSpell 1 - {self.spell_1}\n'
		if self.spell_2 != '':
			text += f'Spell 2 - {self.spell_2}\n'
		return text

items = []
id_list = []

#&slot=misc - cosmetics
#&slot=melee%2Cprimary%2Csecondary - weapons

if __name__ == '__main__':
	cls()
	while True:
		try:
			print('Searches for spelled items on backpack.tf')
			range_1 = int(input('Search spells from page: '))
			range_2 = int(input('to page:                 '))
		except:
			cls()
			print('Please input a number')
		else:
			break
	try:	
		for x in range(range_1 - 1, range_2):
			cls()
			x += 1
			print(f'Processing page {x} of {range_2}...\nCTRL + C to stop')
			for line in get(f'https://backpack.tf/classifieds?page={x}&slot=misc').text.splitlines():
				if 'data-spell_1' in line: #change 1 to 2 for only double spells
					try: 
						data_id = line.split('data-id="')[1].split('"')[0]
						if data_id in id_list: 
							continue
						id_list.append(data_id)
						name = line.split('title="')[1].split('"')[0]
						price = line.split('data-listing_price="')[1].split('"')[0]
						spell_1 = line.split('data-spell_1="Halloween Spell:')[1].split('"')[0]
						spell_2 = ''
						if 'data-spell_2' in line:
							spell_2 = line.split('data-spell_2="Halloween Spell:')[1].split('"')[0]
						item = Item(name, price, spell_1, spell_2)
					except:
						continue
					items.append(item)
	finally:
		with open('items.txt', 'a') as file:
			file.write(f'pages {range_1} - {range_2}\n\n')
			count = len(items)
			if count == 0: 
				file.write('No items found\n\n')
				input('No items found')
			else: 
				for item in items:
					file.write(f'{str(item)}\n')
				file.write(f'{count} items\n\n')
				input(f'Success! {count} items saved in items.txt')
