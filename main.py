import discord
from discord.ext import commands
import botc_helper
import ast
import random
import copy

intents = discord.Intents().all()
bot = commands.Bot(command_prefix="!", intents = intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    bot.script_og = []
    bot.script = []
    bot.game = []
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
    bot.script_og = ast.literal_eval(arg)
    await ctx.reply("Script loaded")

@bot.command()
async def new_game(ctx, number, player_role_id):
    counts = []
    delta_outsiders = 0
    bot.script = copy.deepcopy(bot.script_og)
    bot.game = []
    player_ids = []
    for member in ctx.guild.members:
        for role in member.roles:
            if int(role.id) == int(player_role_id):
                player_ids.append(member.id)
    counts = copy.deepcopy(bot.count_to_numbers[int(number)])
    demon_id = random.choice(player_ids)
    demon_role = random.choice(bot.script[3]["roles"])
    bot.game.append(botc_helper.Player(demon_role, False, demon_id, ctx.guild.get_member(demon_id).display_name))
    player_ids.remove(bot.game[0].discord_id)
    if bot.game[0].role == "lil_monsta":
        bot.game = []
        counts[2] += 1
        counts[3] = 0
        player_ids.append(demon_id)
    
    delta_outsiders = 0
    for i in range(counts[2]):
        curr_minion_id = random.choice(player_ids)
        minion_role = random.choice(bot.script[2]["roles"])
        if demon_role == "fang_gu":
            delta_outsiders += 1
        if minion_role == "baron":
            delta_outsiders += 2
        elif minion_role == "balloonist":
            delta_outsiders += 1
        elif minion_role == "vigormortis":
            delta_outsiders -= 1
        elif minion_role == "godfather":
            delta_outsiders += random.choice([1, -1])

        bot.game.append(botc_helper.Player(minion_role, False, curr_minion_id, ctx.guild.get_member(curr_minion_id).display_name))
        player_ids.remove(curr_minion_id)
        bot.script[2]["roles"].remove(minion_role)

    counts[1] += delta_outsiders
    for i in range(counts[1]):
        curr_outsider_id = random.choice(player_ids)
        curr_outsider_role = random.choice(bot.script[1]["roles"])
        bot.game.append(botc_helper.Player(curr_outsider_role, True, curr_outsider_id, ctx.guild.get_member(curr_outsider_id).display_name))
        player_ids.remove(curr_outsider_id)
        bot.script[1]["roles"].remove(curr_outsider_role)

    for i in range(len(player_ids)):
        curr_townsfolk_id = random.choice(player_ids)
        curr_townsfolk_role = random.choice(bot.script[0]["roles"])
        bot.game.append(botc_helper.Player(curr_townsfolk_role, True, curr_townsfolk_id, ctx.guild.get_member(curr_townsfolk_id).display_name))
        player_ids.remove(curr_townsfolk_id)
        bot.script[0]["roles"].remove(curr_townsfolk_role)

    await ctx.reply(bot.game)

token = open("token.txt", "r")
bot.run(token.readline())