import json
import os 
import discord
from discord.ext import commands

jfile = open("wallets.json", "r+", encoding='utf-8')
info = json.load(jfile)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='>', intents=intents)

print("running on: ", info["token"])

@bot.command()
async def test(ctx):
    print("test")
    await ctx.send('test')

@bot.command()
async def acc(ctx):
    print("acc")
    #commands.UserConverter("481159373620510731")
    await ctx.send(info["wallets"][str(ctx.author.id)])

@bot.command()
async def give(ctx, user:discord.User, amnt:float):
    print("give")
    try:
        if not(str(user.id) == str(ctx.author.id)):
            if not((info["wallets"][str(ctx.author.id)]-amnt)<0):
                info["wallets"][str(ctx.author.id)]-=-amnt
                info["wallets"][str(user.id)]+=amnt
                await ctx.send("sent "+str(amnt)+" to "+str(user))
            else:
                await ctx.send("imagine")
        else:
                await ctx.send("imagine")
    except ValueError:
        await ctx.send("wrong ammount")
    except commands.errors.UserNotFound:
        await ctx.send("wrong user")
    except commands.errors.CommandInvokeError:
        await ctx.send("user not registered")
            
@bot.command()
async def bankgive(ctx, user:discord.User, amnt:float):
    print("bankgive")
    if(discord.utils.get(ctx.guild.roles, name='zaufany') in ctx.author.roles):
        info["wallets"][str(user.id)]+=float(amnt)
        print("    bankgave ", amnt, " to", str(user))
    else: await ctx.send("you cannot bankgive")

@bot.command()
async def register(ctx):
    print("register")
    y={str(ctx.author.id):1000}
    info["wallets"].update(y)
    print(json.dumps(info))
    

bot.run(info["token"])

jfile.seek(0)
jfile.truncate()
json.dump(info, jfile)
jfile.close()