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

@register('test')
async def get_tour(command, msg, user, channel, *args, **kwargs):
    url = msg.split(' ')[0]
    base_url = "https://api.challonge.com/v1/"
    current_time = datetime.datetime.now()
    last_saturday = str(current_time.date()
        - datetime.timedelta(days=current_time.weekday())
        + datetime.timedelta(days=5, weeks=-1))
    parts = []

    payload = {'api_key':api_key, 'state':'pending'}
    if subdomain:
        payload.update({'subdomain': subdomain})
    tours_get = requests.get(base_url + "tournaments.json", params=payload)
    if '200' in str(tours_get.status_code):
        if url in [tours_get.json()[tour]['tournament']['url'] for tour in range(len(tours_get.json()))]:
            for t in tours_get.json():
                t = t['tournament']
                if t['url'] not in [url]:
                    continue

                parts_get = requests.get(base_url + "tournaments/" + str(t['id']) + "/participants.json", params={'api_key':api_key})
                if '200' in str(parts_get.status_code):
                    for p in parts_get.json():
                        p = p['participant']
                        if p['name'].lower() not in get_users(kwargs['full_msg']).values():
                            parts.append(p['name'])
                    await channel.send("**NOT IN DISCORD:** {0}".format(', '.join(parts)))
        else:
            await channel.send(bold("INVALID TOURNAMENT"))