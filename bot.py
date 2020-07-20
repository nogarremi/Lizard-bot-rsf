import discord
import os
import json

import interface
from utilities import read_db,settings_exist
from secret import bot

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))
    print('-------------------------------')
    for guild in client.guilds:
        print('Joined guild %s' % guild)


# Yaksha
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Check if the channel is in the DB
    # Add it if it isn't
    if not settings_exist(message.guild.id):
        await chan.send("Oops, I'm broken")
        print("Oops, I'm broken")

    # Get prefix for the guild
    prefix = read_db('prefix-nog', message.guild.id)

    if not message.content.startswith(prefix):
        return

    for command in client.commands.keys():
        msg = message.content # The message
        user = message.author # The author

        # Check if the message begins with a command
        if msg[1:].lower().startswith(command.lower()):
            # Remove the command from the start
            msg = msg[len(command)+1:].strip()
            command = command.lower()
            
            # Await the interface calling the command
            response = await client.interface.call_command(command, msg, user, message.channel, guild=message.guild.id, full_msg=message)
            
            # If there is a response, send it
            if response:
                await message.channel.send(response)
            break

# Yaksha
def main():
    # Pull in a seperate config
    config = json.loads(open(os.path.join(os.path.dirname(__file__), './bots.json')).read())

    # Grab our commands
    client.commands = config.get('common_commands', {}).copy()
    client.commands.update(config.get('admin_commands', {}))

    client.config = config

    # Start our interface for our commands and Discord
    client.interface = interface.Interface(config, client.commands)

    # Start the bot
    client.run(bot)

# If main is here, run main
if __name__ == '__main__':
    main()