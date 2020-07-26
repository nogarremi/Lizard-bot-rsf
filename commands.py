from utilities import (register, bold, get_users, read_db, save_db, settings_exist)
from pprint import pformat

from secret import api_key
import requests
import json
import datetime

# All @register() are a product of reviewing Yaksha
# See utilities.register for more information

@register('help-nog')
async def help(command, msg, user, channel, *args, **kwargs):
    return "This is a helpful message: You can do it. You can win. Yes Yes Yes!"

@register('ping-nog')
async def ping(command, msg, user, channel, *args, **kwargs):
    return "Pong!"

# Admin Commands
@register('botrole')
async def botrole(command, msg, user, channel, *args, **kwargs):
    for role in user.roles:
        if role.id == read_db(command, kwargs['guild']):
            return "The bot role is {0}".format(bold(role.name))

@register('edit')
async def edit(command, msg, user, channel, *args, **kwargs):
    params = msg.split(' ')
    full_msg = kwargs['full_msg'] # Allows us to access the role_mentions

    editable_command = params[0].lower() # Lower the command we are editing
    params.remove(editable_command) # Remove the command from the params

    # Rejoin the rest of the parameters with spaces
    db_message = ' '.join(params) # The message we send to the Database

    # Grab just the BigInt part of bot_role
    if editable_command in ['botrole']:
        # Allow @everyone to be a botrole
        if '@everyone' in params:
            db_message = str(full_msg.guild.default_role.id)
        else:
            db_message = str(full_msg.role_mentions[0].id)

    save_db(editable_command, db_message, kwargs['guild']) # Save the new message to the proper setting in a given guild
    return "The new {0} is: {1}".format(bold(editable_command), bold(db_message)) # Print the new message for a given setting

@register('prefix-nog')
async def prefix(command, msg, user, channel, *args, **kwargs):
    return "The prefix is: {0}".format(read_db(command, kwargs['guild']))

@register('challonge')
async def challonge(command, msg, user, channel, *args, **kwargs):
    subcommand = msg.split(' ')[0]
    tour_url = msg.split(' ')[1]
    subdomain = read_db(command, kwargs['guild'])
    base_url = "https://api.challonge.com/v1/tournaments/"

    if subdomain:
        tour_url = subdomain + '-' + tour_url
    parts_get = requests.get(base_url + tour_url + "/participants.json", params={'api_key':api_key})
    if '200' in str(parts_get.status_code):
        if subcommand in 'checkin':
            discord_parts = []
            checked_parts = []
            for p in parts_get.json():
                p = p['participant']
                if not p['checked_in']:
                    checked_parts.append(p['name'])
                if p['name'].lower() not in get_users(kwargs['full_msg']).values():
                    discord_parts.append(p['name'])
            return_msg = "**NOT CHECKED IN:** {0}\n**NOT IN DISCORD:** {1}".format(', '.join(checked_parts), ', '.join(discord_parts))
        elif subcommand in 'seed':
            return_msg = "Not implemented yet"
        else:
            return_msg = "Invalid command"
        await channel.send(return_msg)