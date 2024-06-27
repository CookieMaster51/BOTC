import discord
from discord.ext import commands
import discord.utils
import logging

class botc_bot:
    def __init__(self, prefix, token_file_name, log_file) -> None:    
        intents = discord.Intents().all() # Might make this better than all of the intents
        self.bot = commands.Bot(command_prefix=prefix, intents = intents) 
        self.handler = logging.FileHandler(filename=log_file, encoding='utf-8', mode='w')
        self.token_file_name = token_file_name
        
    def run(self):
        token = open(self.token_file_name, "r") # You aint getting my token you sneaky boi
        self.bot.run(token.readline(), log_handler=self.handler)

    def normal_message(self, alert_id):
        @self.bot.event
        async def on_message(message):

            await self.bot.process_commands(message) # VERY VERY FUCKING IMPORTANT

            await self.check_help(message, alert_id)

    def ready(self):
        @self.bot.event
        async def on_ready():
            print("ready")
    
    def purge(self):
        @self.bot.command()
        async def purge_vcs(ctx):
            for channel in discord.utils.get(ctx.guild.categories, name="PRIVATEVCS").channels: # Goes through every channel in the privatevcs category
                if "create" not in channel.name:
                    await channel.delete() # Gets rid of it

    def mute(self, role_id):
        @self.bot.command()
        async def mute_all(ctx):
            for player in ctx.guild.get_role(role_id).members:
                if player.voice:
                    await player.edit(mute=True)

    def unmute(self, role_id):
        @self.bot.command()
        async def unmute_all(ctx):
            for player in ctx.guild.get_role(role_id).members:
                if player.voice:
                    await player.edit(mute=False)

    def collect_people(self):
        @self.bot.command()
        async def collect(ctx, channel_id):
            for member in ctx.guild.members:
                if member.voice != None:
                    await member.move_to(discord.utils.get(ctx.guild.channels, id = int(channel_id)))

    def distribute_to(self):
        @self.bot.command()
        async def distribute(ctx, category_id):
            to_move = [member for member in ctx.guild.members if member.voice != None]
            available = [priv_vc for priv_vc in discord.utils.get(ctx.guild.categories, id = int(category_id)).channels if type(priv_vc) == discord.VoiceChannel]
            if len(to_move) <= len(available):
                for index, member in enumerate(to_move):
                    await member.move_to(available[index])
            else:
                await ctx.reply("Too many people too move")

    def sus(self):
        @self.bot.command()
        async def jansus(ctx):
            await ctx.channel.send(file=discord.File('jansus.png'))

    async def check_help(self, message, alert_id):
        if not message.author.bot:
            if type(message.channel) == discord.channel.DMChannel:
                if "help" in message.content:
                    alert_usr = self.bot.get_user(alert_id)
                    await alert_usr.send(f"{message.author.mutual_guilds[0].get_member(message.author.id).display_name} needs help")

    def voice_stated(self):
        @self.bot.event
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
        


