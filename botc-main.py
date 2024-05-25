# TODO: Add more logic, riot, legion, atheist
#       Change the discord bot intents
#       Make existing logic look better
#       Add json exporting
#       Testing of weirder scripts
#       Add storyteller customisation

import discord
from discord.ext import commands
import botc_helper
import ast
import random
import copy
import discord.utils
import logging

intents = discord.Intents().all() # Might make this better than all of the intents
bot = commands.Bot(command_prefix="!", intents = intents) 
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

@bot.event
async def on_ready(): # Mostly constants
    print(f"Logged in as {bot.user}")
    bot.script_og = []
    bot.script =  []
    bot.game = botc_helper.Game()
    bot.evil_knows = True
    bot.choir_boy = False
    bot.huntsman = False
    bot.legion = False
    bot.riot = False
    bot.king = ""
    bot.damsel = False

    bot.count_to_numbers = {5:[3,0,1,1],
                            6:[3,1,1,1],
                            7:[5,0,1,1],
                            8:[5,1,1,1],
                            9:[5,2,1,1],
                            10:[7,0,2,1],
                            11:[7,1,2,1],
                            12:[7,2,2,1],
                            13:[9,0,3,1],
                            14:[9,1,3,1],
                            15:[9,2,3,1]}
    

@bot.command()
async def set_script(ctx, *, arg):
    bot.script_og = ast.literal_eval(arg) # Just kinda loads the script, idk what to say
    await ctx.reply("Script loaded")

@bot.command()
async def new_game(ctx, number, player_role_id):
    # Just doing some re-setting of variables
    counts = []
    delta_outsiders = 0
    bot.script = copy.deepcopy(bot.script_og)
    bot.game = botc_helper.Game()
    player_ids = [] 
    is_demon = True
    bot.evil_knows = True 
    bot.choir_boy = False
    bot.huntsman = False
    bot.damsel = False
    bot.legion = False
    bot.riot = False
    bot.king = ""

    for member in ctx.guild.members: # Goes through every member
        for role in member.roles: # Goes through their roles
            if int(role.id) == int(player_role_id): # Checks if that role is the one specified
                player_ids.append(member.id) # Makes a list of players with that role

    counts = copy.deepcopy(bot.count_to_numbers[int(number)]) # Gets the number of different types of players from the master copy

    demon_id = random.choice(player_ids)
    demon_role = random.choice(bot.script[3]["roles"])
    bot.game.demon.append(botc_helper.Player(demon_role, False, demon_id, ctx.guild.get_member(demon_id).display_name)) # Adds a demon to the game
    player_ids.remove(demon_id)

    if bot.game.demon[0].role == "lil_monsta": # Logic tested and works (i think)
        is_demon = False
        bot.game = botc_helper.Game()
        counts[2] += 1
        counts[3] = 0
        player_ids.append(demon_id)
    
    delta_outsiders = 0
    for i in range(counts[2]): # Goes through the number of minions that should be in play
        curr_minion_id = random.choice(player_ids)
        minion_role = random.choice(bot.script[2]["roles"])

        if demon_role == "fang_gu": # More edge-case logic, might want to make this neater later, also need testing
            delta_outsiders += 1
        if minion_role == "baron":
            delta_outsiders += 2
        elif minion_role == "balloonist":
            delta_outsiders += 1
        elif minion_role == "vigormortis":
            delta_outsiders -= 1
        elif minion_role == "godfather":
            delta_outsiders += random.choice([1, -1]) # Fuck you storyteller; it's random

        bot.game.minions.append(botc_helper.Player(minion_role, False, curr_minion_id, ctx.guild.get_member(curr_minion_id).display_name)) # Add the minion
        player_ids.remove(curr_minion_id)
        bot.script[2]["roles"].remove(minion_role)

    counts[1] += delta_outsiders # Adding changes to the outsider count due to minions
    if counts[1] < 0: # Making sure there aren't negative outsider totals
        counts[1] = 0

    for i in range(counts[1]): # Adding outsiders, copy-pasted logic
        curr_outsider_id = random.choice(player_ids)
        curr_outsider_role = random.choice(bot.script[1]["roles"])
        bot.game.outsiders.append(botc_helper.Player(curr_outsider_role, True, curr_outsider_id, ctx.guild.get_member(curr_outsider_id).display_name))
        player_ids.remove(curr_outsider_id)
        bot.script[1]["roles"].remove(curr_outsider_role)

    for i in range(len(player_ids)): # Looping through rest of the player ids to assign them townsfolk 
        curr_townsfolk_id = random.choice(player_ids)
        curr_townsfolk_role = random.choice(bot.script[0]["roles"])
        player_ids.remove(curr_townsfolk_id)

        if curr_townsfolk_role == "choirboy": ## ~~~ I PRAY THIS WORKS, MORE TESTING NEEDED ~~~
            bot.choir_boy = True
            if bot.king == "":
                if len(bot.game.townsfolk) > 0:
                    pos = random.randint(0, len(bot.game.townsfolk)-1)
                    bot.game.townsfolk[pos].role = "king"
                    bot.king = bot.game.townsfolk[pos].discord_nick
                    bot.script[0]["roles"].remove("king")
                else:
                    king_id = random.choice(player_ids)
                    bot.game.townsfolk.append(botc_helper.Player("king", True, king_id, ctx.guild.get_member(king_id).display_name))
                    bot.king = ctx.guild.get_member(king_id).display_name
                    bot.script[0]["roles"].remove("king")

        
        if curr_townsfolk_role == "huntsman":
            if not bot.damsel:
                bot.huntsman = True
                bot.damsel = True
                if len(bot.game.townsfolk) > 0:
                    bot.game.townsfolk[random.randint(0, len(bot.game.townsfolk))].role = "damsel"
                    bot.script[0]["roles"].remove("damsel")
                else:
                    damsel_id = random.choice(player_ids)
                    bot.game.townsfolk.append(botc_helper.Player("damsel", True, damsel_id, ctx.guild.get_member(damsel_id).display_name))
                    bot.script[0]["roles"].remove("damsel")

        if curr_townsfolk_role == "king":
            bot.king = ctx.guild.get_member(curr_townsfolk_id).display_name

        if curr_townsfolk_role == "damsel":
            bot.damsel = True

        if curr_townsfolk_role == "poppy_grower":
            bot.evil_knows = False

        bot.game.townsfolk.append(botc_helper.Player(curr_townsfolk_role, True, curr_townsfolk_id, ctx.guild.get_member(curr_townsfolk_id).display_name))
        bot.script[0]["roles"].remove(curr_townsfolk_role)

    if is_demon:
        bluffs = []
        for i in range(3): # loops through the 3 bluffs
            bluff = random.choice(bot.script[0]["roles"]) # get a random townsfolk role
            bot.script[0]["roles"].remove(bluff) 
            bluffs.append(bluff)

        for index, demon in enumerate(bot.game.demon):
            bot.game.demon[index].bluffs = bluffs # Give it to all of the demons

    await ctx.reply(bot.game) # Sends a message in the channel to show the grimoir

@bot.command()
async def purge_vcs(ctx):
    for channel in discord.utils.get(ctx.guild.categories, id = 1187372621029986325).channels: # Goes through every channel in the privatevcs category
        if "create" not in channel.name:
            await channel.delete() # Gets rid of it

@bot.command()
async def mute_all(ctx):
    for player in ctx.guild.get_role(1168613786685550734).members:
        if player.voice:
            await player.edit(mute=True)

@bot.command()
async def unmute_all(ctx):
    for player in ctx.guild.get_role(1168613786685550734).members:
        if player.voice:
            await player.edit(mute=False)

@bot.command()
async def send_roles(ctx):
    bot.game.combine()
    for person in bot.game.full_game: # Loops through everyone
        person_channel = discord.utils.get(ctx.guild.channels, name = f"{person.discord_nick.lower()}-home") # Gets their private channel
        if not person.alignment_good and bot.evil_knows: # Checks if the person is good and that evil should learn who eachother are
            if person in bot.game.demon:
                await person_channel.send(content = f"You are the {person.role}\nYour minions are {str(''.join(list(bot.game.minions[x].discord_nick for x in range(len(bot.game.minions)))))}")
                if bot.king != "":
                    await person_channel.send(content = f"{bot.king} is your king")
            else:
                await person_channel.send(content = f"You are the {person.role}\nYour demon is {bot.game.demon[0].discord_nick}")
                if bot.damsel:
                    await person_channel.send(content = f"There is a damsel")
        else:
            await person_channel.send(content = f"You are the {person.role}")

@bot.command()
async def collect(ctx, channel_id):
    for member in ctx.guild.members:
        if member.voice != None:
            await member.move_to(discord.utils.get(ctx.guild.channels, id = int(channel_id)))

@bot.command()
async def distribute(ctx, category_id):
    to_move = [member for member in ctx.guild.members if member.voice != None]
    available = [priv_vc for priv_vc in discord.utils.get(ctx.guild.categories, id = int(category_id)).channels if type(priv_vc) == discord.VoiceChannel]
    if len(to_move) <= len(available):
        for index, member in enumerate(to_move):
            await member.move_to(available[index])
    else:
        await ctx.reply("Too many people too move")

@bot.command()
async def jansus(ctx):
    await ctx.channel.send(file=discord.File('jansus.png'))

@bot.event
async def on_message(message):

    await bot.process_commands(message) # VERY VERY FUCKING IMPORTANT

    if not message.author.bot:
        if type(message.channel) == discord.channel.DMChannel:
            if "help" in message.content:
                bobby = bot.get_user(485511317164130304)
                await bobby.send(f"{message.author.mutual_guilds[0].get_member(message.author.id).display_name} needs help")


@bot.event
async def on_voice_state_update(member, before, after):
    if after.channel != None:
        TWO_PLAYER_CREATE = discord.utils.get(after.channel.guild.channels, name = "2 person create").id
        THREE_PLAYER_CREATE = discord.utils.get(after.channel.guild.channels, name = "3 person create").id
        FOUR_PLAYER_CREATE = discord.utils.get(after.channel.guild.channels, name = "4 person create").id

        if after.channel.id == TWO_PLAYER_CREATE:
            await after.channel.guild.create_voice_channel(f"2 player {member.display_name}", category = discord.utils.get(after.channel.guild.categories, name = "PRIVATEVCS"), user_limit = 2)

        if after.channel.id == THREE_PLAYER_CREATE:
            await after.channel.guild.create_voice_channel(f"3 player {member.display_name}", category = discord.utils.get(after.channel.guild.categories, name = "PRIVATEVCS"), user_limit = 3)

        if after.channel.id == FOUR_PLAYER_CREATE:
            await after.channel.guild.create_voice_channel(f"4 player {member.display_name}", category = discord.utils.get(after.channel.guild.categories, name = "PRIVATEVCS"), user_limit = 4)

    if before.channel != None:
        if before.channel.category.id == discord.utils.get(before.channel.guild.categories, name = "PRIVATEVCS").id:
            if len(before.channel.members) == 0 and "create" not in before.channel.name: # Checks if there are 0 players in that vc
                await before.channel.delete()
    

token = open("token.txt", "r") # You aint getting my token you sneaky boi
bot.run(token.readline())
