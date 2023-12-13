from typing import Optional
from realdb import (
    create_player, create_item, create_monster,
    create_market, update_player_xp, get_stats,
    update_player_level, update_market,
    update_inventory, check_if_exist,
    add_to_market, find_item_by_id, display_market,
    update_player_coin, check_inventory, clear_market
)
import discord
from discord.ui import Button, View
from discord import app_commands
from discord.ext import commands
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = f""
client = MongoClient(uri, server_api=ServerApi('1'))


bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())


@bot.command(name='hello', help='Prints a welcome message')
async def hello(ctx):
    await ctx.send('Hello! I am your simple Discord bot.')

@bot.command(name="crplayer")
async def Create_player(ctx):

    member = ctx.message.author
    player_exist = check_if_exist(f"{member}")
    print(player_exist)

    if player_exist == True:
        embed = discord.Embed(title=f"@{member} already Exist", color= discord.Color.green())
        await ctx.send(embed=embed)
        
        
    else:
        create_player(f"{member}")
        player_stats = get_stats(f"{member}")

        embed = discord.Embed(title=f"@{member} ID Created", color= discord.Color.green())
        embed.set_thumbnail(url=member.avatar)
        embed.add_field(name="Name", value=f"{player_stats['name']}")
        embed.add_field(name="Level", value=f"{player_stats['level']}")
        embed.add_field(name="Health", value=f"{player_stats['health']}")
        embed.add_field(name="XP", value=f"{player_stats['xp']}")
        embed.add_field(name="Attack Damage", value=f"{player_stats['strength']}")
        embed.add_field(name="Defeated Monster", value=f"{player_stats['defeated_monster']}")

        await ctx.send(embed=embed)
        print(member)

# @bot.command(name="Market")
# async def market(ctx):

#     member = ctx.message.author
#     embed = discord.Embed(title="Hamster Market", description= "", color = discord.Color.green())

@bot.command(name="TestExp")
async def testExp(ctx, xp):
    member = ctx.message.author
    update_player_xp(f"{member}", xp)
    
    player_data = get_stats(f"{member}")

    if player_data:
        embed = discord.Embed(title=f"Total EXP: {player_data['xp']}", color=discord.Color.green())

        await ctx.send(embed=embed)

@bot.command(name="TestCoin")
async def testCoin(ctx, coin):
    member = ctx.message.author
    update_player_coin(f"{member}", coin)

    player_data = get_stats(f"{member}")

    if player_data:
        embed = discord.Embed(title=f"Total coins: {player_data['coins']}", color=discord.Color.green())

        await ctx.send(embed=embed)

@bot.command(name='stats')
async def display_stats(ctx):

    member = ctx.message.author
    player_data = get_stats(f"{member}")

    if player_data:
        # Creating an embed
        embed = discord.Embed(title=f"Stats for {player_data['name']}", color=discord.Color.green())
        embed.add_field(name="Level", value=player_data['level'], inline=True)
        embed.add_field(name="Health", value=player_data['health'], inline=True)
        embed.add_field(name="XP", value=player_data['xp'], inline=True)
        embed.add_field(name="Strength", value=player_data['strength'], inline=True)
        embed.add_field(name="Defeated Monsters", value=player_data['defeated_monster'], inline=True)

        await ctx.send(embed=embed)
    else:
        await ctx.send(f"Player {member} not found.")

@bot.command(name='finditem')
async def findItem(ctx, ID):
    
    itemdata = find_item_by_id(ID)

    if itemdata:
        # Creating an embed
        embed = discord.Embed(title=f"Stats for {itemdata['name']}", color=discord.Color.green())
        embed.add_field(name="Description", value=itemdata['Description'], inline=False)
        embed.add_field(name="Type", value=itemdata['Type'], inline=False)
        embed.add_field(name="Cost", value=itemdata['Cost'], inline=False)
        embed.add_field(name="Rarity", value=itemdata['Rarity'], inline=False)
        embed.add_field(name="DropRate", value=itemdata['DropRate'], inline=False)

        await ctx.send(embed=embed)
    else:
        await ctx.send(f"Player {itemdata} not found.")

@bot.command(name='marketdisplay')
async def MarketDisplay(ctx):
    itemdata_list = display_market()
    button = Button(label="Buy", style=discord.ButtonStyle.green)
    view = View()
    view.add_item(button)
    if itemdata_list:
        for itemdata in itemdata_list:
            # Creating an embed for each item
            embed = discord.Embed(title=f"Buy {itemdata['name']}", color=discord.Color.green())
            embed.add_field(name="Description", value=f"{itemdata['Description']}"[:20], inline=True)
            embed.add_field(name="Type", value=f"{itemdata['Type']}"[:20], inline=True)
            embed.add_field(name="Rarity", value=f"{itemdata['Rarity']}"[:20], inline=True)
            embed.add_field(name="DropRate", value=f"{itemdata['DropRate']}"[:20], inline=True)
            embed.add_field(name="Cost", value=f"{itemdata['Cost']}"[:20], inline=True)

            # Add other fields here based on your item data

            await ctx.send(embed=embed)
            await ctx.send(view=view)
    else:
        await ctx.send("Market not found.")

@bot.command(name='resetmarket')
async def resetMarket(ctx):
    clear_market()
    update_market()
    await ctx.send("Market Reset Complete")

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


#--------------------------------------------------------------------------------------

# add_to_market("TestItem1", "A Sword", "Sword", "common", 0, 100)


# find_item_by_id("6572e7d19adf5717af3909ea")
#update_market()
#clear_market()
#display_market()
# personal bot
# bot.run("")
bot.run('')