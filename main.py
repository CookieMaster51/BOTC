# TODO: Add more logic, king, choirboy, riot, legion, huntsman
#       Change the discord bot intents
#       Make existing logic look better
#       Add json exporting
#       Testing of weirder scripts

import discord
from discord.ext import commands
import botc_helper
import ast
import random
import copy
import discord.utils

intents = discord.Intents().all() # Might make this better than all of the intents
bot = commands.Bot(command_prefix="!", intents = intents) 

@bot.event
async def on_ready(): # Mostly constants
    print(f"Logged in as {bot.user}")
    bot.script_og = []
    bot.script =  []
    bot.game = botc_helper.Game()
    bot.is_poppygrower = False
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
    bot.PRIVATE_VCS_CATEGORY_ID = 1186598911096406046

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

    for member in ctx.guild.members: # Goes through every member
        for role in member.roles: # Goes through their roles
            if int(role.id) == int(player_role_id): # Checks if that role is the one specified
                player_ids.append(member.id) # Makes a list of players with that role

    counts = copy.deepcopy(bot.count_to_numbers[int(number)]) # Gets the number of different types of players from the master copy

    demon_id = random.choice(player_ids)
    demon_role = random.choice(bot.script[3]["roles"])
    bot.game.demon.append(botc_helper.Player(demon_role, False, demon_id, ctx.guild.get_member(demon_id).display_name)) # Adds a demon to the game
    player_ids.remove(demon_id)

    if bot.game.demon[0].role == "lil_monsta": # UNTESTED LOGIC, hopefully works
        is_demon = False
        bot.game = []
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
        bot.game.townsfolk.append(botc_helper.Player(curr_townsfolk_role, True, curr_townsfolk_id, ctx.guild.get_member(curr_townsfolk_id).display_name))
        player_ids.remove(curr_townsfolk_id)
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
    for channel in discord.utils.get(ctx.guild.categories, id = bot.PRIVATE_VCS_CATEGORY_ID).channels: # Goes through every channel in the privatevcs category
        await channel.delete() # Gets rid of it

@bot.command()
async def send_roles(ctx):
    bot.game.combine()
    for person in bot.game.full_game:
        person_channel = discord.utils.get(ctx.guild.channels, name = f"{person.discord_nick.lower()}-home")
        if not person.alignment_good and not bot.is_poppygrower:
            if person in bot.game.demon:
                await person_channel.send(content = f"You are the {person.role}\nYour minions are {str(''.join(list(bot.game.minions[x].discord_nick for x in range(len(bot.game.minions)))))}")
            else:
                await person_channel.send(content = f"You are the {person.role}\nYour demon is {bot.game.demon[0].discord_nick}")
        else:
            await person_channel.send(content = f"You are the {person.role}")

@bot.event
async def on_voice_state_update(member, before, after):
    TWO_PLAYER_CREATE = 1186328181758763169
    THREE_PLAYER_CREATE = 1186604174130024559
    FOUR_PLAYER_CREATE = 1186604215343255573
    

    if after.channel.id == TWO_PLAYER_CREATE:
        await after.channel.guild.create_voice_channel(f"2 player {member.display_name}", category = discord.utils.get(after.channel.guild.categories, id = bot.PRIVATE_VCS_CATEGORY_ID), user_limit = 2)

    if after.channel.id == THREE_PLAYER_CREATE:
        await after.channel.guild.create_voice_channel(f"3 player {member.display_name}", category = discord.utils.get(after.channel.guild.categories, id = bot.PRIVATE_VCS_CATEGORY_ID), user_limit = 3)

    if after.channel.id == FOUR_PLAYER_CREATE:
        await after.channel.guild.create_voice_channel(f"4 player {member.display_name}", category = discord.utils.get(after.channel.guild.categories, id = bot.PRIVATE_VCS_CATEGORY_ID), user_limit = 4)


    if before.channel.category.id == bot.PRIVATE_VCS_CATEGORY_ID:
        if len(before.channel.members) == 0: # Checks if there are 0 players in that vc
            await before.channel.delete()
    

token = open("token.txt", "r") # You aint getting my token you sneaky boi
bot.run(token.readline())