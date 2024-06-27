from botc_bot_class import botc_bot

bot = botc_bot("!", "token.txt", "discord.log")

mute_role_id = 1168613786685550734

bot.ready()

bot.unmute(mute_role_id)
bot.mute(mute_role_id)

bot.sus()

bot.normal_message(690615895663575182)

bot.purge()
bot.voice_stated()

bot.collect_people()
bot.distribute_to()

bot.run()