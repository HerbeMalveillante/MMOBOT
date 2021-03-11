import discord
from discord.ext import commands
from configcreator import Config
import asyncio
from log import log
from epicstore_api import EpicGamesStoreAPI
import datetime
import re

config = Config()

def getGames():
    """Récupère les derniers jeux gratuits dans l'epic game store.
    On va 'parser' les données de l'API, c'est à dire récupérer ce
    qui nous intéresse et dégager le reste."""
    
    api = EpicGamesStoreAPI() #On crée un objet api de la part du module epicgamestore. Il faut se référer à la documentation pour comprendre comment ça marche, on le devine pas comme ça
    free_games = api.get_free_games()['data']['Catalog']['searchStore']['elements'] # on utilise une methode de l'objet API qui nous retourne les jeux gratuts, et on navigue dans les dictionnaires pour récupérer les véritables jeux gratuits.
    # ici c'est pareil on est pas censé le deviner la documentation nous le donne. C'est pas le cas de la suite.
    #Ici, free_games est une liste de dictionnaires. Chaque dictionnaire représente un jeu.
    
    
    # à partir d'ici tu te débrouilles lol
    jeuxGratuits = []
    
    for i in free_games :
        parsedGame = parseGame(i)
        if parsedGame != None :
            jeuxGratuits.append(parsedGame)
    
    return jeuxGratuits
        
def parseGame(game):
    """
    Cette fonction prend en entrée un dictionnaire obtenu avec la methode api.get_free_games() vue précédemment.
    Elle retourne un objet de type GameObject que nous avons créé plus haut.
    """
    name = game['title'] # on récupère simplement le bon attribut du dictionnaire
    
    productSlug = game['productSlug']
    gameLink = f"https://www.epicgames.com/store/fr/product/{productSlug}"
    
    description = game['description']
    keyImages = game['keyImages'] # keyImages est une liste d'au moins deux images.
    # Si le jeu est activement en promotion, il y aura six images, dont les deux premières seront
    # l'image large et l'image haute. On en récupère les liens : 
    imageWide = keyImages[0]['url']
    imageTall = keyImages[1]['url']
    seller = game['seller']['name']
    originalPrice = game['price']['totalPrice']['fmtPrice']['originalPrice']
    
    try : 
        startDate = game['promotions']['promotionalOffers'][0]['promotionalOffers'][0]['startDate'] # ceci ne va marcher que sur le jeu actuellement gratuit.
        endDate = game['promotions']['promotionalOffers'][0]['promotionalOffers'][0]['endDate'] # c'est pour ça qu'on le met dans un try.
        currentlyFree = True # on en profite pour définir la variable pour voir si il est gratuit actuellement sur true
    except : 
        try :
            startDate = game['promotions']['upcomingPromotionalOffers'][0]['promotionalOffers'][0]['startDate'] # ceci ne marchera que sur un jeu bientôt gratuit.
            endDate = game['promotions']['upcomingPromotionalOffers'][0]['promotionalOffers'][0]['endDate'] # c'est pour ça qu'on le met dans un try.
            currentlyFree = False
        except:
            #print("Le jeu sélectionné n'est ni gratuit, ni bientôt gratuit.")
            return None # un return met fin à l'execution du code de la fonction.
            

    
    # il faut savoir que si les jeux ne sont pas activement en promotion (au moment du test, jurassic world evolution et torchlight II
    # qui étaient tous deux en réduction il y a quelques temps sont encore présents dans la liste des jeux), leurs attributs seront buggés.
    # grace à des try except qui détectent quand le programme déclenche une erreur, on peut déterminer si un jeu est gratuit, bientôt gratuit ou
    # just buggé. Si il est juste buggé la fonction retourne None.
    
    
    # et on va retourner un dictionnaire avec tous les attributs qu'on a parsé
    dicoJeu = {}
    dicoJeu['name']=name
    dicoJeu['currentlyFree']=currentlyFree
    dicoJeu['gameLink'] = gameLink
    dicoJeu['description'] = description
    dicoJeu['startDate'] = startDate
    dicoJeu['endDate'] = endDate
    dicoJeu['imageWide'] = imageWide
    dicoJeu['imageTall'] = imageTall
    dicoJeu['seller'] = seller
    dicoJeu['originalPrice'] = originalPrice
    
    return dicoJeu



class MiscCommandsCog(commands.Cog):
	def __init__(self,bot):
		self.bot = bot
	
	@commands.command(name="epic", aliases = ["epicgames"], description = "Displays the currently free games available on the EPIC GAME STORE")
	async def epic(self, ctx, arg="list"):
		games = getGames()
		
		
		#await ctx.send(games)
		
		if arg == "list":
			
			indexListString = "|".join([str(i) for i in range(len(games))])
			embed = discord.Embed(title=f"FREE GAMES ON THE EPIC GAME STORE", description = f"Use the command `{config.prefix}epic <{indexListString}>` to see the corresponding game.", colour=config.colour, timestamp=datetime.datetime.utcnow())
			embed.set_thumbnail(url="https://cdn2.unrealengine.com/Unreal+Engine%2Feg-logo-filled-1255x1272-0eb9d144a0f981d1cbaaa1eb957de7a3207b31bb.png")
			embed.set_footer(text=self.bot.user.name + ' - requested by ' +str(ctx.author), icon_url=ctx.author.avatar_url)
			
			embed.add_field(name="Game index :", value="\n".join([f"`{i} | {games[i]['name']}`" for i in range(len(games))]))
			
			await ctx.send(embed=embed)
			return
		else :
		
			try :
				arg = int(arg) # si l'entrée peut être un chiffre
			except :
				await ctx.send(f"Invalid argument. Usage : `{config.prefix}epic [list|<1...9>]`")
				return
			
			if arg not in [i for i in range(len(games))] :
				await ctx.send(f"Game number {arg} not found. Check `{config.prefix}epic list` to check the available games.")
				return

		
		
			game = games[arg]
		
			validurl = re.compile(r"^(?:http(s)?:\/\/)?[\w.-]+(?:\.[\w\.-]+)+[\w\-\._~:/?#[\]@!\$&'\(\)\*\+,;=.]+$")
			


			embed = discord.Embed(title=f"FREE GAMES ON THE EPIC GAME STORE", description = f"Use the command `{config.prefix}epic list` to see all the available games.", colour=config.colour, timestamp=datetime.datetime.utcnow())
			if validurl.match(game['imageWide']) is not None :
				embed.set_thumbnail(url=game['imageWide'])
			else :
				embed.set_thumbnail(url='https://worldofvoz.files.wordpress.com/2020/01/http-error-404-not-found.png')
			embed.set_footer(text=self.bot.user.name + ' - requested by ' +str(ctx.author), icon_url=ctx.author.avatar_url)
			embed.add_field(name="Game name :", value = game['name'])
			embed.add_field(name="Game seller : ", value=game['seller'], inline = False)
			value = "Currently Free" if game["currentlyFree"] == True else "Soon to be free"
			embed.add_field(name="Game state :", value = f"{value} (previously {game['originalPrice']})", inline = False)
			embed.add_field(name="Link to the game page :", value = f"[Click me]({game['gameLink']})", inline = False)
			embed.add_field(name="Promotion dates :", value=f"{game['startDate'][:10]} to {game['endDate'][:10]}", inline = False)
			if validurl.match(game['imageWide']) is not None :
				embed.add_field(name="Images :", value = f"[Wide image]({game['imageWide']})\n[Tall image]({game['imageTall']})", inline=False)

			
			await ctx.send(embed=embed)
			
			
		log(f"{ctx.author} asked about the free games")

def setup(bot):
	bot.add_cog(MiscCommandsCog(bot))
