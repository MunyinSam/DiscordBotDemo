from datetime import datetime, timezone
from bson import ObjectId
from mongoengine import Document, fields, connect
import discord
from discord import app_commands
from discord.ext import commands
import random
import pprint
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Connect to MongoDB
uri = ''
connect('data', host='')
client = MongoClient(uri, server_api=ServerApi('1'))

class Player(Document):
    name = fields.StringField(required=True)
    levels = fields.IntField()
    xp = fields.IntField()
    health = fields.IntField()
    strength = fields.IntField()
    inventory = fields.ListField(fields.StringField())
    sessions = fields.ListField(fields.DateTimeField())
    defeated_monster = fields.IntField()
    gacharoll = fields.IntField()
    coins = fields.IntField()

class Item(Document):
    name = fields.StringField(required=True)
    desc = fields.StringField()
    item_type = fields.StringField()
    rarity = fields.StringField()
    cost = fields.IntField()
    drop_rate = fields.FloatField()
    # image = fields.ImageField()

class Monster(Document):
    name = fields.StringField(required=True)
    desc = fields.StringField()
    levels = fields.IntField()
    health = fields.IntField()
    strength = fields.IntField()
    expDrop = fields.IntField()
    moneyDrop = fields.IntField()

class Zone(Document):
    name = fields.StringField(required=True)
    desc = fields.StringField()
    types = fields.StringField()
    rarity = fields.StringField()

class Market(Document):
    item_stock = fields.ListField(fields.ReferenceField(Item))

printer = pprint.PrettyPrinter()

# Create a Player instance and save to the database

def create_player(name):
    player_data = {
        'name': name,
        'levels': 1,
        'xp': 0,
        'health': 10,
        'strength': 1,
        'inventory': [],
        'sessions': [datetime.now(timezone.utc)],
        'defeated_monster': 0,
        'coins' : 0
    }
    player = Player(**player_data)
    player.save()

def create_item():
    Item_data = {
        'name' : "Sword",
        'desc' : "Default item",
        #Item_type = fields.StringField()
        'rarity' : "Common",
        'cost' : 30,
        'drop_rate' : 1.5
        #'image' : None
    }

    item = Item(**Item_data)
    item.save()

def create_monster():
    monster_data = {
        'name' : "Slime",
        'desc' : "A normal Slime",
        'levels': 1,
        'health' : 3,
        'strength' : 0,
        'expDrop' : 3,
        'moneyDrop' : 1
    }

    monster = Monster(**monster_data)
    monster.save()

def create_market():
    market_data = {}
    
    market = Market(**market_data)
    market.save()

# Player Functions

def update_player_level(player_name):
    retrieved_player = Player.objects(name=player_name).first()

    # Check if player exists before updating
    if retrieved_player:
        # Update player data and save
        retrieved_player.levels += 1
        retrieved_player.health += 2
        retrieved_player.save()
        print("Player updated level successfully")
    else:
        print("Player not found")

def update_player_xp(player_name, expPoint):
    
    retrieved_player = Player.objects(name=player_name).first()

    # Check if player exists before updating
    if retrieved_player:
        # Update player data and save
        retrieved_player.xp += int(expPoint)
        retrieved_player.save()
        print("Player updated xp successfully")
    else:
        print("Player not found")

    if retrieved_player.xp == 100:
        retrieved_player.xp -= 100
        retrieved_player.save()
        update_player_level(player_name)

def update_player_coin(player_name, coin):

    retrieved_player = Player.objects(name=player_name).first()

    # Check if player exists before updating
    if retrieved_player:
        # Update player data and save
        retrieved_player.coins += int(coin)
        retrieved_player.save()
        print("Player updated coin successfully")
    else:
        print("Player not found")   

def get_stats(player_name):
    #print(player_name)
    retrieved_player = Player.objects(name=player_name).first()
    
    if retrieved_player:
        name = retrieved_player.name
        level = retrieved_player.levels
        hp = retrieved_player.health
        xp = retrieved_player.xp
        damage = retrieved_player.strength
        dft_monster = retrieved_player.defeated_monster
        coins = retrieved_player.coins
        print(f"ID : {name}")
        print(f"Current Level: {level}")
        print(f"EXP : {xp}")
        print(f"Health : {hp}")
        print(f"Damage : {damage}")
        print(f"Monster Defeated : {dft_monster}")
        
        return {
            "name": name,
            "level": level,
            "health": hp,
            "xp": xp,
            "strength": damage,
            "defeated_monster": dft_monster,
            "coins" : coins
        }
    else:
        return None

def check_inventory(player_name):

    retrieved_player = Player.objects(name=player_name).first()

    if retrieved_player:
        inventory = retrieved_player.inventory
        print(f"Items: {inventory}")
    else:
        print("Player not found")

# Market Functions

def update_inventory(command, player_name, item):

    if command == "Buy":
        
        player = Player.objects(name=player_name).first()

        if player:
            player.inventory.append(item)

            player.save()
            print(f"{player_name} Successfully bought {item}")
    
    
    elif command == "Sell": 
        
        Player.objects(name=player_name).update(pull__inventory=item)
        print(f"{player_name} Successfully sold {item}")
        
        #Users.objects(username='some_user').update(pull_all__following=['one_string', 'another_string'])        

def check_if_exist(player_name):

    player = Player.objects(name=player_name).first()

    if player:
        print("Player already Exist")
        return True
    else:
        print("Player doesn't Exist")
        return False

def add_to_market(name, desc, type, rarity, cost, dr):

    weapon = Item(name=f"{name}", desc=f"{desc}", item_type=f"{type}", rarity=f"{rarity}", cost=cost, drop_rate=dr)
    weapon.save()

    # Get or create a market instance
    market = Market.objects.first()
    if not market:
        market = Market(item_stock=[])

    # Add the item reference to the market
    
    market.item_stock.append(weapon)
    market.save()    

# data2 = client.data # mongodb automakes db for you (doesnt exist)
# person_collection = data2.person_collection

# def find_player():
#     player = data2.find()
#     printer.pprint(player)

def find_item_by_id(object_id_str):
    try:
        # Convert the string ObjectId to ObjectId type
        object_id = ObjectId(object_id_str)

        # Find the document by ObjectId
        item = Item.objects.get(id=object_id)    

        print('Found document:', item)
        print('ID :', item.id)
        print('name:', item.name)
        print('Description :', item.desc)
        print('Type :', item.item_type)
        print('Cost :', item.cost)
        print('Rarity :', item.rarity)
        print('DropRate :', item.drop_rate)

        return {
            "name": item.name,
            "Description": item.desc,
            "Type": item.item_type,
            "Cost": item.cost,
            "Rarity": item.rarity,
            "DropRate": item.drop_rate
        }
  
    except Item.DoesNotExist:
        print('Document not found')

def display_market():
    try:
        # Find the market by its ID
        #market = Market.objects.get(id="657484bef6480675c9949f81")
        market = Market.objects().first()

        itemdata_list = []

        # Iterate through item_stock and collect item details
        for item_ref in market.item_stock:
            item = Item.objects.get(id=item_ref.id)
            itemdata = {
                "name": item.name,
                "Description": item.desc,
                "Type": item.item_type,
                "Cost": item.cost,
                "Rarity": item.rarity,
                "DropRate": item.drop_rate
            }
            itemdata_list.append(itemdata)

        return itemdata_list

    except Market.DoesNotExist:
        print("Market not found")
        return [] 

def update_market():
    
    market = Market.objects().first()

    if market:
        random_items = [get_random_item_reference() for _ in range(4)]
        market.item_stock.extend(random_items)

        market.save()
        print("Items added successfully.")
    else:

        new_market = Market(item_stock=[])
        
        random_items = [get_random_item_reference() for _ in range(4)]
        new_market.item_stock.extend(random_items)

        new_market.save()
        print("New market created and items added successfully.")
    
def clear_market():
    # Retrieve the Market document
    market = Market.objects().first()

    # Check if the document exists
    if market:
        # Delete all documents in the Market collection
        Market.objects().delete()
        print("Market cleared successfully.")
    else:
        print("Market not found.")

def get_random_item_reference():
    # Query the Item collection for a random item
    random_item = Item.objects().limit(1).skip(random.randint(0, Item.objects().count() - 1)).first()
    return random_item