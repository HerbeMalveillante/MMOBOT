import json
import datetime

# Version number. Changed manually.
version = "0.1"


class Config(object):
#Loading the config options from the config file and creating a class
	def __init__(self):
		with open('config.txt') as json_file:
			data = json.load(json_file)
			self.prefix = data['prefix']
			self.description = data['description'] + version
			self.token = data['token']  # token of the bot
			self.botActivity = data['botActivity'] + version
			self.colour = int(data['color'])
			self.timeout = float(data["timeout"])
			self.boottime = datetime.datetime.now().timestamp()
			self.admins = [412425659483160579,417013673442279434]


class EmojiList(object):
	def __init__(self):
		self.emojis = {
		"Exp" : ":star:",
		"Gold" : "<:coins:789965630434181120>",
		"Energy" : ":zap:",
		"Diamonds" : "<:diamond:796663370002071582>",
		"Weapon" : ":dagger:",
		"Armor" : "<:armor:796664730827751424>",
		"Backpack" : "<:backpack:796665117235478558>",
		"Attack" : ":muscle:",
		"Defense" : ":shield:",
		"Stamina" : ":runner:",
		
		"Wood" : ":wood:",
		"Fabric" : ":scroll:",
		"Iron":"<:iron:796670376293826590>",
		"Rock" : ":rock:",
		"Orb" : ":crystal_ball:",
		"Emerald" : "<:emerald:796671885525123122>",
		"Oil" : "<:oil_bottle:796675410397757460>",
		"Obsidian" : "<:obsidian:796676716802080808>:",
		"Seeds":":seedling:",
		"Antimatter" : "<:antimatter:796678615202529300>"
		
		}
