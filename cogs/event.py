import asyncio
import discord
from discord.ext import commands
import sqlite3
import random


class Event(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        db = sqlite3.connect("eco.sqlite")
        cursor = db.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS main (
            user_id INTERGER, wallet INTERGER, bank INTERGER
        )''')
        print("Ping.py is ready!")
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        
        author = message.author
        db = sqlite3.connect("eco.sqlite")
        cursor = db.cursor()
        cursor.execute(f"SELECT user_id FROM main WHERE user_id = {author.id}")
        result = cursor.fetchone()
        if result is None:
            sql = ("INSERT INTO main(user_id, wallet, bank) VALUES (?, ?, ?)")
            val = (author.id, 100, 0)
            cursor.execute(sql, val)
        
        db.commit()
        cursor.close()
        db.close()
    

async def setup(bot):
    await bot.add_cog(Event(bot))




