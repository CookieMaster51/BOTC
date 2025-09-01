"""Features that allow BOTC and other larger events via discord to go smoother"""

import logging
import discord
from discord.ext import commands
import discord.utils


class BotcBot:
    """Class of the bot itself"""
    def __init__(self, prefix, token_file_name, log_file) -> None:
        intents = discord.Intents().all() # Might make this better than all of the intents
        self.bot = commands.Bot(command_prefix=prefix, intents = intents)
        self.handler = logging.FileHandler(filename=log_file, encoding='utf-8', mode='w')
        self.token_file_name = token_file_name

    def run(self):
        """Runs the code"""
        token = open(self.token_file_name, "r", encoding="utf8")
        # You aint getting my token you sneaky boi
        self.bot.run(token.readline(), log_handler=self.handler)

    def normal_message(self, alert_id):
        """Handles the checking of DMs for help"""
        @self.bot.event
        async def on_message(message):

            await self.bot.process_commands(message) # VERY VERY FUCKING IMPORTANT

            await self.check_help(message, alert_id)

    def ready(self):
        """Prints when the bot is ready, 
        function already implemented in the log file so is redundant and only for testing"""
        @self.bot.event
        async def on_ready():
            print("ready")

    def purge(self):
        """Removes all empty private VCs"""
        @self.bot.command()
        async def purge_vcs(ctx):
            # Goes through every channel in the privatevcs category
            for channel in discord.utils.get(ctx.guild.categories, name="PRIVATEVCS").channels:
                if "create" not in channel.name:
                    await channel.delete() # Gets rid of it

    def mute(self, role_id):
        """Server mutes everyone with the role corrisponding to the ID given"""
        @self.bot.command()
        async def mute_all(ctx):
            for player in ctx.guild.get_role(role_id).members:
                if player.voice:
                    await player.edit(mute=True)

    def unmute(self, role_id):
        """Un-server mutes everyone"""
        @self.bot.command()
        async def unmute_all(ctx):
            for player in ctx.guild.get_role(role_id).members:
                if player.voice:
                    await player.edit(mute=False)

    def collect_people(self):
        """Moves everyone into a specific channel LIMITED TO 10 PEOPLE"""
        @self.bot.command()
        async def collect(ctx, channel_id):
            channel = discord.utils.get(ctx.guild.channels, id = int(channel_id))
            for member in ctx.guild.members:
                if member.voice is not None:
                    await member.move_to(channel)

    def distribute_to(self):
        """Moves people into VCs in a specific category at 1 person per VC"""
        @self.bot.command()
        async def distribute(ctx, category_id):
            to_move = [member for member in ctx.guild.members if member.voice is not None]
            available = []

            possible_vcs = discord.utils.get(ctx.guild.categories, id = int(category_id)).channels
            for possible_vc in possible_vcs:
                if isinstance(possible_vc, discord.VoiceChannel):
                    available.append(possible_vc)

            if len(to_move) <= len(available):
                for index, member in enumerate(to_move):
                    await member.move_to(available[index])
            else:
                await ctx.reply("Too many people too move")

    def sus(self):
        """sus pic is posted ;)"""
        @self.bot.command()
        async def jansus(ctx):
            await ctx.channel.send(file=discord.File('jansus.png'))
    
    def ballsquote(self):
        """balls quote is posted"""
        @self.bot.command()
        async def bobaballs(ctx):
            await ctx.channel.send(file=discord.File('balls.png'))

    async def check_help(self, message, alert_id):
        """Checks if any DMs have the word help"""
        if not message.author.bot:
            if isinstance(message.channel, discord.channel.DMChannel):
                if "help" in message.content:
                    alert_usr = self.bot.get_user(alert_id)
                    person = message.author.mutual_guilds[0].get_member(message.author.id)
                    await alert_usr.send(f"{person.display_name} needs help")

    def voice_stated(self):
        """Used for creation of private VCs"""
        @self.bot.event
        async def on_voice_state_update(member, before, after):
            if after.channel is not None:
                guild = after.channel.guild
                two_player_create = discord.utils.get(guild.channels, name = "2 person create").id
                three_player_create = discord.utils.get(guild.channels, name = "3 person create").id
                four_player_create = discord.utils.get(guild.channels, name = "4 person create").id
                priv_vc_cat = discord.utils.get(guild.categories, name = "PRIVATEVCS")

                if after.channel.id == two_player_create:
                    name = f"2 player {member.display_name}"
                    await guild.create_voice_channel(name, category = priv_vc_cat, user_limit = 2)

                if after.channel.id == three_player_create:
                    name = f"3 player {member.display_name}"
                    await guild.create_voice_channel(name, category = priv_vc_cat, user_limit = 3)

                if after.channel.id == four_player_create:
                    name = f"4 player {member.display_name}"
                    await guild.create_voice_channel(name, category = priv_vc_cat, user_limit = 4)

            if before.channel is not None:
                guild = before.channel.guild
                priv_vc_cat = discord.utils.get(guild.categories, name = "PRIVATEVCS")
                if before.channel.category.id == priv_vc_cat.id:
                    if len(before.channel.members) == 0 and "create" not in before.channel.name:
                        # Checks if there are 0 players in that vc
                        await before.channel.delete()
