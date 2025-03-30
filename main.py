import discord
from discord.ext import commands
from random import choice, shuffle
bot = commands.Bot(command_prefix='!')
teams = {}
words = {
    "tonnerre" : "éclair",
    "déodorant": "parfum",
    "bonbon": "sucette",
    "Netflix": "Youtube",
    "Guitare": "Violon",
    "Fanta": "Orangina",
    "Ail": "Ognion",
    "Sieste": "Sommeil",
    "Papillon": "Oiseau",
    "Piment": "Wasabi"
}
words_civil = ["tonnerre", "déodorant", "bonbon", "Netflix", "Guitare", "Fanta", "Ail", "Sieste", "Papillon", "Piment"]

game = False
civils = []
undercovers = []
mw = []
allplayers = []
died_undercovers = []
died_mw = []
civilchoiced = ""
waitingformw = False
word_civil = ""

def end():
    global game
    global civils
    global undercovers
    global mw
    global allplayers
    global died_undercovers
    global died_mw
    global civilchoiced
    global waitingformw
    global word_civil
    game = False
    civils = []
    undercovers = []
    mw = []
    allplayers = []
    died_undercovers = []
    died_mw = []
    civilchoiced = ""
    waitingformw = False
    word_civil = ""

@bot.event
async def on_ready():
    print("Bot Prêt")
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game('Undercover'))

@bot.command()
async def newteam(ctx, teamsname,  *members: discord.Member):
    if len(members) >= 3:
        teams[teamsname] = members
        await ctx.send("Equipe Créée")
    else:
        await ctx.send("Vous avez besoin d'au moins 3 joueurs (faites bien attention, la commande est !newteam [nom de la team] [membres sous forme @...]")
        return

@bot.command()
async def newgame(ctx, teamsname, nbundercover, nbmw):
    players = {}
    global game
    global civils
    global undercovers
    global mw
    global allplayers
    global died_mw
    global civilchoiced
    global word_civil
    global teams
    nbundercover = int(nbundercover)
    nbmw = int(nbmw)
    if game is False:
        if len(teams[teamsname]) <= nbundercover+nbmw or nbundercover + nbmw == 0:
            await ctx.send("Il y a soit trop d'undercover et de Mr White Soit il y en n'a 0")
            return
        game = True
        for i in teams[teamsname]:
            civils.append(i)
        if nbundercover > 0:
            for i in range(0, nbundercover):
                civilchoiced = choice(civils)
                undercovers.append(civilchoiced)
                civils.remove(civilchoiced)

        if nbmw > 0:
            for i in range(0, nbmw):
                civilchoiced = choice(civils)
                mw.append(civilchoiced)
                civils.remove(civilchoiced)
        for i in civils:
            players[i] = "civil"
        for i in undercovers:
            players[i] = "undercover"
        for i in mw:
            players[i] = "mw"
        word_civil = choice(words_civil)
        for i in civils:
            await i.send(f"Votre mot est **{word_civil}**,\nil vous est interdit de le divulguer avant la fin de la partie,\ndurant la partie vous n'avez pas le droit de dire un mot de la même famille")
        for i in undercovers:
            await i.send(f"Votre mot est **{words[word_civil]}**,\nil vous est interdit de le divulguer avant la fin de la partie,\ndurant la partie vous n'avez pas le droit de dire un mot de la même famille")
        for i in mw:
            await i.send("Vous êtes **Mr White**,\nnous n'avez pas de mot, si vous êtes éliminé, vous pouvez dire le mot que vous pensez que les civils ont")

        await ctx.send("La Partie est lancée")
        for key,value in players.items():
            allplayers.append(key)
        shuffle(allplayers)
        phrase = "l'ordre : "
        while players[allplayers[0]] == "mw":
            shuffle(allplayers)
        for i in range(0, len(allplayers)):
            phrase += allplayers[i].mention + " "
        await ctx.send(phrase)

    else:
        await ctx.send("Une partie est déja en cours")
        return

@bot.command()
async def helpundercover(ctx):
    print("I'll help you")
    await ctx.send("!newteam [nom de la team sans espace] [les membre sous forme @..]\n!newgame [nom de la team] [nombre undercover] [nombre mister white]\n!dernierechance [mot, si composé, comme pain de mie, écrire pain-de-mie]\n!kill [joueur sous forme @...]")

@bot.command()
async def kill(ctx, pseudo: discord.Member):
    global game
    global words
    global word_civil
    if game is False:
        ctx.send("Pas de Partie en cours")
        return
    global waitingformw
    if waitingformw is True:
        await ctx.send("Attendez que Mr White dise le mot qu'il pense être celui des civils")
        return
    global died_undercovers
    if pseudo in allplayers:
        allplayers.remove(pseudo)
        await ctx.send(pseudo.mention + " a été tué")
        if pseudo in civils:
            await ctx.send("C'était un civil")
            civils.remove(pseudo)
            await pseudo.send("Vous êtes mort, veuilllez donc éviter de parler")
        if pseudo in undercovers:
            await ctx.send("C'était un undercover")
            died_undercovers.append(pseudo)
            undercovers.remove(pseudo)
            await pseudo.send("Vous êtes mort, veuilllez donc éviter de parler")

        if pseudo in mw:
            await ctx.send("C'était un Mr White, qu'il écrive le mot qu'il pense etre celui des civils avec !dernierechance [mot]")
            died_mw.append(pseudo)
            mw.remove(pseudo)
            waitingformw = True
            return
        if len(mw) <= 0 and len(undercovers) <= 0:
            await ctx.send(f"Il n'y a plus d'Undercover ni de Mr White, les civils ont gagné,\nLes Mots étaient {word_civil} pour les civils et {words[word_civil]} pour le(s) undercover(s)")
            game = False
            end()
            return
        if len(mw) + len(civils) + len(died_mw) <= 1 and len(undercovers) > 0:
            phrase_deux = ""
            for i in undercovers:
                phrase_deux += i.mention + " "
            for i in died_undercovers:
                phrase_deux += i.mention + " "
            await ctx.send("Les Undercovers ont gagné, il(s) étai(en)t, " + phrase_deux + f", Félicitations !\nLes Mots étaient {word_civil} pour les civils et {words[word_civil]} pour le(s) undercover(s)")
            game = False
            end()
            return
        if len(allplayers) <= 2 and len(mw) == 1:
            ctx.send(mw[0].mention + " était un Mr White,\nQuel mot pense tu être celui des Civils ?\n(réponds en !dernierechance [mot])")
            waitingformw = True
            return

        await ctx.send("Il reste "+ str(len(undercovers)) + " Undercovers et " + str(len(mw)) + " Mr White")

@bot.command()
async def dernierechance(ctx, word):
    global died_mw
    word = word.lower()
    if ctx.message.author in died_mw:
        global game
        global civils
        global undercovers
        global mw
        global allplayers
        global died_undercovers

        global civilchoiced
        global waitingformw
        global word_civil
        global words
        died_mw.remove(ctx.message.author)
        if word == word_civil:
            global waitingformw
            phrase_quatre = ""
            for i in undercovers:
                phrase_quatre += i.mention
            for i in died_undercovers:
                phrase_quatre += i.mention
            await ctx.send("C'était bien ce mot, Bravo Mr White a gagné")
            await ctx.send("Le(s) undercovers étai(en)t "+ phrase_quatre)
            game = False
            end()
            return
        else:
            await ctx.send("ce n'est pas le bon mot, vous avez perdu")
            await ctx.message.author.send("Vous êtes mort, veuilllez donc éviter de parler")

            waitingformw = False
            if len(mw) <= 0 and len(undercovers) <= 0:
                await ctx.send(f"Il n'y a plus d'Undercover ni de Mr White, les civils ont gagné,\nLes Mots étaient {word_civil} pour les civils et {words[word_civil]} pour le(s) undercover(s)")
                game = False
                end()
                return
            if len(mw) + len(civils) + len(died_mw) <= 1 and len(undercovers) > 0:
                phrase_deux = ""
                for i in undercovers:
                    phrase_deux += i.mention + " "
                for i in died_undercovers:
                    phrase_deux += i.mention + " "
                await ctx.send("Le(s) Undercover(s) a/ont gagné, il(s) étai(en)t, " + phrase_deux + f", Félicitations !\nLes Mots étaient {word_civil} pour les civils et {words[word_civil]} pour le(s) undercover(s)")
                game = False
                end()
                return
            if len(allplayers) <= 2 and len(mw) == 1:
                ctx.send(mw[0].mention + " était un Mr White,\nQuel mot pense tu être celui des Civils ?\n(réponds en !dernierechance [mot])")
                waitingformw = True
                return
    else:
        await ctx.send("Vous n'êtes pas Mr White ou bien vous n'êtes pas mort")
        return
@newgame.error
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("la commande est sous forme !newgame [nom de la team] [nombre Undercover] [nombre Mister White]")
        return
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send("Soit L'équipe n'existe pas, faites !newteam [nom de la team] [les membres sous forme @...]\nSoit l'erreur est ailleur")
        return
    print(error)


token = ""
print("Lancement du Bot...")
bot.run(token)