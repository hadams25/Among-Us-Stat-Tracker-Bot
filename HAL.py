import discord
from discord.ext import commands as com
import json
import psycopg2
import os.path
import sys
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
connection = None

def start():
    global client
    global settings
    global default_settings
    global connection
    
    print("Checking for settings file...")
    #if the settings json file does not exist, create one
    if not path.exists("settings.json"):
        print("Settings file not found. One will be created.")

        with open("settings.json", "w") as j_file:
            json.dump(default_settings, j_file, indent = 4)
    else:
        print("Settings file found.")
    
    with open("settings.json") as j_file:
        settings = json.load(j_file)

    #if settings from file are missing fields, add them from the default settings
    for key in default_settings.keys():
        if not key in settings:
            settings[key] = default_settings[key]
            with open("settings.json", "w") as j_file:
            	json.dump(settings, j_file, indent = 4)
    
    #check if the token field is empty
    if settings["token"] == "":
        print("Token field is empty in settings.json")
        print("Please supply a discord bot token.")
        print("Shutting down...")
        sys.exit()
    
    print("Verifying database connection...")
    #verify connect works
    connection = connect()
    connection.close()
    print("Database connection successful. \nStarting bot...")

    temp = com.Bot(command_prefix = settings["prefix"])

    print("Importing cogs:")
    for filename in os.listdir('./cogs'):
        if filename != "__init__.py" and filename.endswith('.py'):
            temp.load_extension(f'cogs.{filename[:-3]}')

    client.run(settings["token"])

def connect():
    try:
        connection = psycopg2.connect(
                host = settings["host"],
                database = settings["database"],
                user = settings["user"],
                password = settings["password"],
                port = settings["port"],)
    except:
        print("Error connecting to database!")
        print("Check credentials and try again.")
        print("Shutting down...")
        logging.error(traceback.format_exc())
        sys.exit()

    return connection

def table_exists(schema: str, table: str) -> bool:
    """
    Checks if a table with the given schema exists
    Returns a boolean
    """
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("""
    SELECT EXISTS (
        SELECT FROM information_schema.tables 
        WHERE  table_schema = '""" + schema + """'
        AND    table_name   = '""" + table + """'
    );"""
    )

    exists = cursor.fetchall()[0][0]

    connection.close()

    return exists

def create_table(schema: str, table: str):
    """
    Creates a table from the schema and table name given
    """

    connection = connect()
    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE """ + schema + "." + table + """ (
        player     NUMERIC      PRIMARY KEY     NOT NULL,
        crew_games INT                          NOT NULL,
        crew_wins  INT                          NOT NULL,
        imp_games  INT                          NOT NULL,
        imp_wins   INT                          NOT NULL,
        kills      INT                          NOT NULL,
        deaths     INT                          NOT NULL);"""
    )
    connection.commit()
    cursor.close()
    connection.close()

@client.event
async def on_ready():
    global client
    global settings
    global default_settings
    
    print('Logged in as ' + client.user.name)
    print('------')
    game = discord.Game(settings["status"])
    await client.change_presence(status=discord.Status.idle, activity=game)
    print("Currently serving the following guilds:")
    for server in client.guilds:
        print("- " + server.name)

@client.event
async def on_guild_join(guild):
    """
    Make  a new server table when joing a server, if one doesn't already exist
    """
    if not table_exists("servers", guild.id):
        create_table("servers", str(guild.id))

@com.command()
async def ping(self, ctx):
    await ctx.send("Pong!")

if __name__ == '__main__':
    start()
