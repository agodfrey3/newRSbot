import discord
from discord.ext import commands
import asyncio
from bs4 import BeautifulSoup
import urllib.request
import cred

description = '''A Discord Bot for Runescape - Made by RdTo99Swole'''

bot = commands.Bot(command_prefix='!', description=description)

def getInfo():
	a = []
	a.append("Available Commands:")
	a.append("!help OR !info :Shows list of commands - info will show how to use them")
	a.append("!welcome 'NAME' :welcomes someone (just first name)")
	a.append("!stats 'NAME' : gets stats of desired player (max 3 word name)")
	a.append("!price 'ITEM' :gets price of item (max two word item - are any items more than that?)")
	a.append("!rots :gets current Rise of the Six Rotation")
	a.append("!araxxor :gets current araxxor paths")
	a.append("!vorago :gets current vorago rotation")
	return a

def getSkills(user):
	try:
		url = 'http://services.runescape.com/m=hiscore/compare?user1=' + user
		page = urllib.request.urlopen(url)
		soup = BeautifulSoup(page.read(), 'lxml')
		data = soup.findAll('td', class_="playerWinLeft alignleft")
		skills = []
		for x in data:
			soup2 = BeautifulSoup(str(x), 'lxml')
			tag = soup2.find(href=True)
			skill = str(tag)
			index = skill.find(";page=1")
			skills.append(str(skill[int(index)+9:int(index)+11]))
		try:
			skills.pop(0)
		except IndexError:
			return "ERROR"
		return skills
	except urllib.error.HTTPError:
		return "ERROR"


def getRago():
	url = 'http://runescape.wikia.com/wiki/Vorago/Strategies'
	page = urllib.request.urlopen(url)
	soup = BeautifulSoup(page.read(), 'lxml')
	data = soup.find('table', class_="wikitable")
	index = str(data).find("status-active")
	sChar = str(data)[index+15]
	if sChar == 'C':
		return "Cieling Collapse"
	elif sChar == 'S':
		return "Scopulus"
	elif sChar == 'V':
		return "Vitalis"
	elif sChar == 'G':
		return "Green Bomb"
	elif sChar == 'T' and str(data)[index+16] == 'e':
		return "Teamsplit"
	else:
		return "The End"

def getRots():
	url = 'http://runescape.wikia.com/wiki/Barrows:_Rise_of_the_Six'
	page = urllib.request.urlopen(url)
	soup = BeautifulSoup(page.read(), 'lxml')
	data = soup.find('table', class_='wikitable')
	karil = str(data).find('Karil')
	dharok = str(data).find('Dharok')
	ahrim = str(data).find('Ahrim')
	torag = str(data).find('Torag')
	verac = str(data).find('Verac')
	guthan = str(data).find('Guthan')
	brothers = {'Dharok':dharok, 'Karil':karil, 'Ahrim':ahrim,'Torag':torag,'Verac':verac,'Guthan':guthan}
	inOrder = sorted(brothers, key=brothers.__getitem__)
	return inOrder

def getPaths():
	url = 'http://runescape.wikia.com/wiki/Araxxor/Strategies'
	page = urllib.request.urlopen(url)
	soup = BeautifulSoup(page.read(), 'lxml')
	data = soup.find('table', class_='wikitable')
	index = str(data).find("Closed")
	index2 = str(data).find("Open")
	index3 = str(data).find("Open", index2, len(str(data)))
	if(index < index2 and index < index3):
		return "Paths Two and Three are open- Acid and Darkness, oh my!"
	if(index > index2 and index < index3):
		return "Paths One and Three are open- Minions and Darkness, sounds like fun!"
	else:
		return "Paths One and Two are open- Minions and Acid, yum!"

def getPrice(item):
	try:
		str(item).replace(" ", "_")
		print(item)
		url = 'http://runescape.wikia.com/wiki/' + item
		page = urllib.request.urlopen(url)
		soup = BeautifulSoup(page.read(), 'lxml')
		data = soup.find('span', class_='infobox-quantity')
		return data['data-val-each']
	except urllib.error.HTTPError:
		return "ERROR"

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def welcome(message = "Dickhead"):
    """Welcomes Player with a kind message"""
    await bot.say("Hey %s! Sup you piece of shit?" % message)

@bot.command()
async def info():
	"""Shows help"""
	info = getInfo()
	for line in info:
		await bot.say(line)

@bot.command()
async def price(item1, item2 = ""):
	"""Gets G.E. Price of an item"""
	try:
		if str(item2) != '':
			item2 = '_' + str(item2)
			item = str(item1) + str(item2)
		else:
			item = str(item1)
		price = getPrice(item)
		if price == "ERROR":
			await bot.say("Sorry, that item was not found")
		else:
			await bot.say("The price is: " + str(price))
	except TypeError:
		await bot.say("That item is not tradeable! What a shame...")

@bot.command()
async def stats(first, second="", third=""):
	"""Gets a player's stats"""
	if second == '' and third == '':
		player = first
	elif third == '':
		player = first + '_' + second
	else:
		player = first + '_' + second + '_' + third
	lvls = getSkills(player)
	if lvls != "ERROR":
		skills = ['Attack: ' + lvls[0], 'Defense: ' + lvls[1], 'Strength: ' + lvls[2], 'HP: ' + lvls[3],'Ranged: ' \
					+ lvls[4],'Prayer: ' + lvls[5],'Magic: ' + lvls[6],'Cooking: ' + lvls[7], 'Woodcutting: ' + lvls[8], \
					'Fletching: ' + lvls[9],'Fishing: ' + lvls[10],'Firemaking: ' + lvls[11],'Crafting: ' + lvls[12],'Smithing: ' \
					 + lvls[13],'Mining: ' + lvls[14],'Herblore: ' + lvls[15],'Agility: ' + lvls[16],'Thieving: ' + lvls[17], \
					'Slayer: ' + lvls[18],'Farming: ' + lvls[19],'Runecrafting: ' + lvls[20],'Hunter: ' + lvls[21],'Construction: '\
					 + lvls[22],'Summoning: ' + lvls[23],'Dungeoneering: ' + lvls[24],'Divination: ' + lvls[25], \
				 	'Invention: ' + lvls[26]]
		await bot.say( "Stats for: " + player \
					    + '\n' + skills[0] + '\n' + skills[1]+ '\n' + skills[2]+ '\n' + skills[3]+ '\n' + skills[4]+ '\n' + skills[5] \
						+ '\n' + skills[6]+ '\n' + skills[7]+ '\n' + skills[8]+ '\n' + skills[9]+ '\n' + skills[10] \
						+ '\n' + skills[11]+ '\n' + skills[12]+ '\n' + skills[13]+ '\n' + skills[14]+ '\n' + skills[15] \
						+ '\n' + skills[16]+ '\n' + skills[17]+ '\n' + skills[18]+ '\n' + skills[19]+ '\n' + skills[20] \
						+ '\n' + skills[21]+ '\n' + skills[22]+ '\n' + skills[23]+ '\n' + skills[24]+ '\n' + skills[25] \
						+ '\n' + skills[26])
	else:
		await bot.say("Player not found!")

@bot.command()
async def rots():
	"""Gets Rise of the Six Rotation"""
	brothers = getRots()
	east = []
	west = []
	i = 1
	for key in brothers:
		if i % 2 == 0:
			east.append(key)
		else:
			west.append(key)
		i += 1
	await bot.say("-WEST-")
	for bro in west:
		await bot.say('  ' + bro)
	await bot.say("----------")
	await bot.say("-EAST-")
	for bro in east:
		await bot.say('  ' + bro)
	await bot.say("----------")

@bot.command()
async def araxxor():
	"""Gets Araxxor Rotation"""
	currRotation = getPaths()
	await bot.say(currRotation)

@bot.command()
async def vorago():
	"""Gets Vorago Rotation"""
	currRotation = getRago()
	await bot.say("Vorago is currently on: %s" % currRotation)

bot.run(cred.un, cred.pw) 
