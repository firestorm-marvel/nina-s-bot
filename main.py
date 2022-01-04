import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import random
from discord.ext import tasks
import youtube_dl
import asyncio
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path="config")

musics = {}

ytdl = youtube_dl.YoutubeDL

print('Lancement du bot')
bot = commands.Bot(command_prefix='+')

warnings = {}

gif_cat = [ "https://tenor.com/view/cat-cute-adorable-punch-gif-17822730",
    "https://tenor.com/view/cool-cat-gif-18199666",
    "https://tenor.com/view/cat-cool-lit-gif-13999500",
    "https://tenor.com/view/cute-kitty-best-kitty-alex-cute-pp-kitty-omg-yay-cute-kitty-munchkin-kitten-gif-15917800",
    "https://tenor.com/view/cute-kitten-kitten-cat-cats-cattitude-gif-17661396",
    "https://tenor.com/view/kittens-cute-cat-pet-cheeks-gif-16382546"]



co_routine = [ "Abonnez-vous à la chaine de Nina",
    "+help pour toute les commandes",
    "J'ai été coder par Firestorm !",
    "Il m'a programmé en moins de 40h !",
    "https://www.youtube.com/channel/UCQpsZns9PyzJ0cnuFaMzSQA",
    "Le feu ca brule et l'eau ca mouille"]


# gerer les errreurs de toute les commandes.*
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Vous n'avez pas les permissions de faire cette commande !")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Oupssss, je crois qu'il manque un argument.")
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("Ouppsss, aucune commande n'a été trouvé a ce nom, tu peux néanmoins faire la commande +help !")
    elif isinstance(error, commands.CheckFailure):
        ctx.send("Je crois qu'il y a eu une erreur, réessaye s'il-te-plait")
@bot.event
async def on_ready():
    print("Je suis pret !")
    change_status.start()

async def CreateMutedRole(ctx):
    mutedRole = await ctx.guild.create_role(name='Muted', permissions=discord.Permissions(send_messages=False, speak =False))

    for channel in ctx.guild.channels:
        await channel.set_permissions(mutedRole, speak = False, send_messages = False)
    return mutedRole


async def GetMuedRole(ctx):
    roles = ctx.guild.roles
    for role in roles:
        if role == "Muted":
            return role
    return await CreateMutedRole(ctx)


@bot.command(name='cat')
async def cat(ctx):
    await ctx.send(random.choice(gif_cat))

@bot.command(name='pp')
async def pp(ctx, membre : discord.User):
    pp = membre.avatar_url
    await   ctx.send(f"Wow ! Quelle photo de profil !\n {pp}")


@bot.command(name='mute')
@has_permissions(manage_messages=True)
async def mute(ctx, member : discord.Member):
    MutedRole = await GetMuedRole(ctx)
    embed = discord.Embed(title="Mute", description="Un modérateur a frappé !", inline=False, color=0x78EB0C)
    embed.add_field(name="Muté(e)", value=f"L'utilisateur muté est **{member}**", inline=True)
    embed.add_field(name="Modérateur", value=f"le seul est l'unique **{ctx.author}**", inline=True)
    await ctx.send(embed=embed)
    await member.add_roles(MutedRole)

@bot.command(name='unmute')
async def unmute(ctx, member : discord.Member):
    mutedRole = await GetMuedRole(ctx)
    embed = discord.Embed(title="Unmute", description="Un modérateur a frappé !", inline=False, color=0x78EB0C)
    embed.add_field(name="Unmuté(e)", value=f"L'utilisateur unmuté est **{member}**", inline=True)
    embed.add_field(name="Modérateur", value=f"le seul est l'unique **{ctx.author}**", inline=True)
    await member.remove_roles(mutedRole)
    await ctx.send(embed=embed)


@bot.command(name='youtube')
async def youtube(ctx):
    await ctx.send("Vous pouvez retrouvez toutes les videos de Nina sur sa chaine YouTube : https://www.youtube.com/channel/UCQpsZns9PyzJ0cnuFaMzSQA")

@bot.command(name='twitch')
async def twitch(ctx):
    await ctx.send("Vous pouvez retrouvez tous les lives de Nina sur sa chaine Twitch : https://www.twitch.tv/nina_asmr")

@bot.command(name='ping')
async def ping(ctx):
    await ctx.send('Pong! Il y a {0} secondes de latences ! '.format(round(bot.latency, 1)))

@tasks.loop(seconds = 10)
async def change_status():
    game = discord.Game(random.choice(co_routine))
    await bot.change_presence(activity=game)

@bot.command(name='warning')
@commands.has_permissions(manage_messages=True)
async def warning(ctx, membre: discord.Member):
    id = membre.id
    print("le membre n'a pas de warn")

    if id not in warnings:
        warnings[id] = 0

    warnings[id] += 1
    print("ajoute le warn")
    print(warnings[id])

    if warnings[id] == 3:
        await membre.kick()

    pseudo = membre.mention
    await ctx.send(
        f"{pseudo} a recu un warn! Il a recu un total de {warnings[id]} warnings !\n Attention a bien respecter les regles (!regles) !")




@bot.command(name='regles')
async def regles(ctx):
    print("La commande rules a été activé avec succès")
    await ctx.send(
        "**Tout non-respect des règles sera value d'un warn, au bout de 3 warn, vous serez banni.**\n\n-Soyez respectueux envers tout le monde.\n\nPas d’insultes, pas de choses sexuelles, pas de politique en dehors des débats et on ne parle pas des guerres mondiales\n\n-Les pseudos et photos de profil doivent être réglos ! Pas de choses à caractère sexuel, politique, injurieux etc...\n\n-On respecte les modos et on ne s’énerve pas contre les règles et leurs décisions.\n\n-Bien évidemment amusez-vous c’est le but de ce serveur.\n\n Merci de bien vouloir respecter ces regles.")


@bot.command(name='info')
async def info(ctx):
    server = ctx.guild
    members = server.member_count
    message = f"Sur le serveur de Nina, il y a {members} personnes ! "
    await ctx.send(message)


# creation de la comande aide
@bot.command(name='commandes')
async def aide(ctx):
    async def aide(ctx):
        print('lancement de la commande aide')
        embed = discord.Embed(title="Nina's Bot | HELP", description='Toutes les commandes :', color=0x78EB0C,inline=True)
        embed.add_field(name='**Administration**', value='**Les commandes modérateur sont :**', inline=True)
        embed.add_field(name='+ban', value='Bannissement du membre.', inline=False)
        embed.add_field(name='+kick', value='Éjéction du membre.', inline=False)
        embed.add_field(name='+clear', value='Suppression de message groupé.', inline=False)
        embed.add_field(name='+warning', value='Avetissement sur le membre.', inline=False)
        embed.add_field(name='+mute', value='Mute le membre.', inline=False)
        embed.add_field(name='+unmute', value='Unmute le membre.', inline=False)
        embed.add_field(name='**Commande utile ou fun**', value='**Les commandes utiles ou fun sont :**', inline=True)
        embed.add_field(name='+say', value='Repete la phrase mis en argument.', inline=False)
        embed.add_field(name='+info', value='Donne le nombre de bg présent sur le serveur.', inline=False)
        embed.add_field(name='+aide', value='Registre de toute les commandes.')
        embed.add_field(name='+regles', value='Registre de toutes les regles, je te conseille de les lires.',inline=False)
        embed.add_field(name='+coucou', value="Envoie coucou à la personne de ton choix !", inline=False)
        embed.add_field(name='+cat', value="Une image cutie de chat apparait !", inline=False)
        embed.add_field(name='+lovecheck', value="Donne le lovecehck entre toi et une personne de ton choix.",inline=False)
        embed.add_field(name='+ping', value="Envoie le nombre de latence entre le bot  et le serveur", inline=False)
        embed.add_field(name='+youtube', value="Pour retrouver la chaine youtube de Nina le plus vite possible !",inline=False)
        embed.add_field(name='+twitch', value="Pour retrouver la chaine twitch de Nina super rapidement ", inline=False)
        embed.add_field(name='+pp', value="Affiche la photo de profil de l'utilisateur de ton choix !", inline=False)
        embed.add_field(name='+emoji', value="Nomme tout les emojis de la guilde", inline=False)
        await ctx.send(embed=embed)



@bot.command(name='lovecheck')
async def lovecheck(ctx, user : discord.User):
    loveckeck = random.randint(1, 100)

    if user.name == "Nina's Bot" and ctx.author.name == "FirestormMaitreDesOies":
        await ctx.send(f"Le lovecheck entre {ctx.author.mention} et {user.mention} est de 1000% puisque que c'est mon créateur")
    else:
        await ctx.send(f"Le lovecheck entre {ctx.author.mention} et {user.mention} est de {loveckeck}% !")


@bot.command(name='emoji')
async def emoji(ctx):
    emoji_1 = ":Kappa:"
    emoji_2 = ":emoji_1:"
    emoji_3 = ":emoji_2:"
    emoji_4 = ":emoji_5:"
    emoji_5 = ":emoji_6:"
    emoji_6 = ":emoji_7:"

    await ctx.send(f"Dans ce serveur les emojis utilisables sont : {emoji_1},  {emoji_2},  {emoji_3},  {emoji_4},  {emoji_5},  {emoji_6}")


# creation de la commande say
@bot.command(name='say')
async def say(ctx, *texte):
    print(texte)
    await ctx.send(" ".join(texte))


# Creation de la commande +coucou
@bot.command(name='coucou')
async def coucou(ctx, membre : discord.User):
    print("La commande coucou a été activé !")
    await ctx.send(f"**{ctx.author.mention}** passe le coucou à **{membre.mention}** !")




# creatio de la cmd supprimer plusieurs messages
@bot.command(name='clear')
# seulement les admins peuvent utiliser les cmds
@commands.has_permissions(manage_messages=True)
async def supp(ctx, nombre: int):
    messages = await ctx.channel.history(limit=nombre + 1).flatten()
    for message in messages:
        await message.delete()


# gerer les erreurs de la commande bannisements


# creation de la commande Bannisement
@bot.command(name='ban')
@commands.has_permissions(manage_messages=True)
async def ban(ctx, username: discord.User):
    embed = discord.Embed(title="Bannissement", description="Un modérateur a frappé !", inline=False, color=0x78EB0C)
    embed.add_field(name="Banni", value=f"L'utilisateur banni est **{username}**", inline=True)
    embed.add_field(name="Modérateur", value=f"le seul est l'unique **{ctx.author}**    ", inline=True)
    await  ctx.guild.ban(username)
    await ctx.send(embed = embed)



# création de la commande éjéction
@bot.command(name='kick')
@commands.has_permissions(manage_messages=True)
async def kick(ctx, username: discord.User):
    embed = discord.Embed(title="Bannissement", description="Un modérateur a frappé !", inline=False, color=0x78EB0C)
    embed.add_field(name="Ejécter", value=f"L'utilisateur éjécter est **{username}**", inline=True)
    embed.add_field(name="Modérateur", value=f"le seul est l'unique **{ctx.author}**    ", inline=True)
    await  ctx.guild.kick(username)
    await ctx.send(embed = embed)


# on lance notre bot grace au token
bot.run(os.getenv("TOKEN"))
