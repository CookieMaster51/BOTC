"""Runs an instance of the bot"""
from botc_bot_class import BotcBot

bot = BotcBot("!", "token.txt", "discord.log")

MUTE_ROLE_ID = 1168613786685550734

bot.ready()

bot.unmute(MUTE_ROLE_ID)
bot.mute(MUTE_ROLE_ID)

bot.sus()

bot.normal_message(690615895663575182)

bot.purge()
bot.voice_stated()

bot.collect_people()
bot.distribute_to()

bot.run()
