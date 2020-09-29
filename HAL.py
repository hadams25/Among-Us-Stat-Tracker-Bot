import discord
import json
import sqlite3
import os.path
import sys
from sqlite3 import Error
from os import path

client = discord.Client()
settings = {}
default_settings = {
    "token" : "",
    "status" : "",
    "prefix" : "~"
}

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

def start():
    #if the "Servers" directory, doesn't exist, create one
    if not path.exists("Servers"):
        print("Server directory not found. One will be created.")
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

#if __name__ == '__main__':