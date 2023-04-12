import discord
from discord.ext import commands
import asyncio
import os
import sqlite3
import random
import datetime
from discord import Embed



intents = discord.Intents.all()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')

@bot.command()
async def bal(ctx, member: discord.Member=None):
    if member is None:
        member = ctx.author
    
    db = sqlite3.connect("eco.sqlite")
    cursor = db.cursor()

    cursor.execute(f"SELECT wallet, bank FROM main WHERE user_id = {ctx.author.id}")
    bal = cursor.fetchone()

    em = discord.Embed(color=discord.Color.random())
    #em.set_author(name=client.user.name, icon=discord.Embed.Empty, icon_url=client.user.avatar_url)
    em.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
    em.add_field(name="Wallet", value=f"'💸{bal[0]}'")
    em.add_field(name="Bank", value=f"'🏦{bal[1]}'")
    em.add_field(name="Networth", value=f"'💰{bal[0] + bal[1]}'")
    em.set_thumbnail(url="https://pngimg.com/d/bank_PNG3.png")
    em.timestamp = datetime.datetime.now(datetime.timezone.utc)
    await ctx.reply(embed=em)

    #await ctx.send(f"Wallet: {wallet} \nBank: {bank}")


@bot.command()
async def yetimpayi(ctx):
    earnings = random.randint(10, 100)
    db = sqlite3.connect("eco.sqlite")
    cursor = db.cursor()

    cursor.execute(f"SELECT wallet FROM main WHERE user_id = {ctx.author.id}")
    wallet = cursor.fetchone()

    cursor.execute("UPDATE main SET wallet = ? WHERE user_id = ?", (wallet[0] + int(earnings), ctx.author.id))
    await ctx.send(f"WIN **{earnings}**")

    db.commit()
    cursor.close()
    db.close()



@bot.command()
async def bet(ctx):
    bets = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36]
    db = sqlite3.connect("eco.sqlite")
    cursor = db.cursor()
    cursor.execute(f"SELECT wallet FROM main WHERE user_id = {ctx.author.id}")
    wallet = cursor.fetchone()

    try:
        wallet = wallet[0]
    except:
        wallet = wallet

    await ctx.send("n or c?")
    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel
        
    msg = await bot.wait_for("message", timeout= 5, check = check)
    if msg.content.lower() == "n":
        await ctx.send("Choose Number:")
        botBet = random.randint(0, 36) 

        await ctx.send(botBet) #TEST

        def check(userNum):
            return userNum.author == ctx.author and userNum.channel == ctx.channel
        userNum = await bot.wait_for("message", check=check)
        userBetNum = int(userNum.content)

        if int(userNum.content) in bets:
            await ctx.send(f"How much do you want to gamble on {userNum.content}?")

            def check(userBetM):
                return userBetM.author == ctx.author and userBetM.channel == ctx.channel
            userBetM = await bot.wait_for("message", check=check)
            userBetM = int(userBetM.content)
            

            if userBetM <= wallet:
                wallet = wallet - userBetM
                if userBetNum == botBet:
                    wallet = wallet + userBetM*36
                    wonMoney = userBetM*36
                    await ctx.send(f"WIN {wonMoney}")
                    await ctx.send(f"New Balance {wallet}")
                    cursor.execute("UPDATE main SET wallet = ? WHERE user_id = ?", (wallet, ctx.author.id))
                    db.commit()


                else:
                    await ctx.send("Dealer Wins!")
                    await ctx.send(f"New Balance: {wallet}")
                    cursor.execute("UPDATE main SET wallet = ? WHERE user_id = ?", (wallet, ctx.author.id))
                    db.commit()
            
            else:
                await ctx.send(f"You don't have a enough money in your wallet. \nYour Balance: {wallet}")

        else:
            await ctx.send("Wrong Bet.")



    elif msg.content.lower() == "c":
        await ctx.send("Color Bet Options (Not availabe yet)")

    elif msg is None:
        await ctx.send("Next time choose only n or c.")
    else:
        await ctx.send("Next time choose only n or c.")





async def main():
    await load()
    await bot.start("") # TOKEN

asyncio.run(main())




