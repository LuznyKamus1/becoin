#import libs
import json 
import random 
import os 
import discord
from discord.ext import commands

#define vars
ofile = open("../walletjson/info.json","r+",encoding='utf-8')
info = json.load(ofile)

#define commands prefix
bot = commands.Bot(command_prefix='!')

#test if bot responses
@bot.command()
async def test(ctx):
    print("TEST")
    await ctx.send('test')

#check how many becoin does user have
@bot.command()
async def stats(ctx):
    print("STATS")
    try:
        status=info["accounts"][str(ctx.message.author.id)]["balance"]

        if((status)<100):
            await ctx.message.author.send("you are poor ("+str(status)+" becoins)")
        else:
            await ctx.message.author.send("you have "+str(status)+ " becoins")
    except json.decoder.JSONDecodeError:
        print("There was a problem accessing the json data (balance).")
    await ctx.message.delete()

#give specified amount of money to specified user id
@bot.command()
async def give(ctx, user:discord.User, ammount):
    print("GIVE")
    try:
        if((info["accounts"][str(ctx.message.author.id)]["balance"]-float(ammount))<0):
            await ctx.send("you have insufficient ammount of becoins")
        else:
            info["accounts"][str(user.id)]["balance"] += float(ammount)
            info["accounts"][str(ctx.message.author.id)]["balance"] -= float(ammount)
            await ctx.message.author.send("sent " + str(ammount) + " balance" + " to " + str(user))


    except ValueError:
        await ctx.send('wrong ammount')
    await ctx.message.delete()

@bot.command()
async def helpme(ctx):
    print("HELPME")
    await ctx.send("!test                    - bot says test")
    await ctx.send("!stats                   - see ho much money do you hav")
    await ctx.send("!give `user id` `amount` - gives specified amount of money from your account to specified user")
    await ctx.send("for further help contact - apul ajfon#3144")
    await ctx.message.delete()

# @bot.command()
# async def register(ctx):
#     print("REGISTER")
#     if(str(ctx.message.author.id) in info["accounts"]):
#         info["accounts"][str(ctx.message.author.id)]

@bot.command()
async def bankgive(ctx, user:discord.User, ammount):
    print("BANKGIVE")
    if(discord.utils.get(ctx.guild.roles, name="Bankier") in ctx.message.author.roles):
        info["accounts"][str(user.id)]["balance"] += float(ammount)
        print("    good")

    else: print("    bad")
    await ctx.message.delete()

bot.run(info["discordinfo"]["token"])
#save file on exit and close
ofile.seek(0)
ofile.truncate()
json.dump(info, ofile)
ofile.close()