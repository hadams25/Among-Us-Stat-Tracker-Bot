import discord
import json
import psycopg2
import os.path
import sys
from sqlite3 import Error
from os import path

client = discord.Client()
settings = {}
default_settings = {
    "token" : "",
    "status" : "",
    "prefix" : "~",
    "host" : "localhost",
    "database" : "player_data",
    "user" : "postgres",
    "password" : "",
    "port" : "5432"
}

def start():
    #if the "Servers" directory, doesn't exist, create one
    if not path.exists("player_data.db"):
        print("Player database not found. One will be created.")
        os.mkdir("Servers")

    #if the settings json file does not exist, create one
    if not path.exists("settings.json"):
        print("Settings file not found. One will be created.")

        with open("settings.json", "w") as j_file:
            json.dump(default_settings, j_file)
    
    with open("settings.json") as j_file:
        settings = json.load(j_file)

    #if settings from file are missing fields, add them from the default settings
    for key in default_settings.keys():
        if not key in settings:
            settings[key] = default_settings[key]
    
    #check if the token field is empty
    if settings["token"] == "":
        print("Token field is empty in settings.json")
        print("Please supply a discord bot token.")
        print("Shutting down...")
        sys.exit()
    
    client.run(settings["token"])

def database_check():

@client.event
async def on_ready():
    print('Logged in as ' + client.user.name)
    print('------')
    game = discord.Game(settings["status"])
    await client.change_presence(status=discord.Status.idle, activity=game)
    print("Currently serving the following guilds:")
    for server in client.guilds:
        print("- " + server.name)

@client.event
async def on_guild_join(guild):
    original_dir = os.getcwd()
    os.chdir(original_dir + "/Servers")
    if not path.exists(guild.id + " - " + guild.name + ".db"):
        create_connection(guild.id + " - " + guild.name + ".db")




if __name__ == '__main__':
    start()