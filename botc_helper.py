import discord
class Player:
    def __init__(self, role:str, alignment_good:bool, discord_id:int, discord_nick:str, has_ghost_voted:bool = False, is_dead:bool = False, reminders:list = []):
        self.role = role
        self.discord_id = discord_id
        self.has_ghost_voted = has_ghost_voted
        self.is_dead = is_dead
        self.reminders = reminders
        self.alignment_good = alignment_good
        self.discord_nick = discord_nick

    def __repr__(self) -> str:
        return f"name: {self.discord_nick}; role : {self.role}\n"
    