import discord
class Player:
    def __init__(self, role:str, alignment_good:bool, discord_id:int, discord_nick:str, has_ghost_voted:bool = False, is_dead:bool = False, reminders:list = [], bluffs:list = []):
        self.role = role
        self.discord_id = discord_id
        self.has_ghost_voted = has_ghost_voted
        self.is_dead = is_dead
        self.reminders = reminders
        self.alignment_good = alignment_good
        self.discord_nick = discord_nick
        self.bluffs = bluffs

    def __repr__(self) -> str:
        return f"name: {self.discord_nick}; role : {self.role}" if self.bluffs == [] else f"name: {self.discord_nick}; role : {self.role}; bluffs : {self.bluffs}"

class Game:
    def __init__(self) -> None:
        self.demon = []
        self.minions = []
        self.outsiders = []
        self.townsfolk = []
        self.full_game = []

    def combine(self):
        self.full_game = self.demon + self.minions + self.outsiders + self.townsfolk
    
    def __repr__(self) -> str:
        return str(list(map(str, self.demon)) + list(map(str, self.minions)) + list(map(str, self.outsiders)) + list(map(str, self.townsfolk))) + "\n"
