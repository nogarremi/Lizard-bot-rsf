from utilities import (register, bold, read_db, save_db, settings_exist)
import asyncio
import random
import pprint
import json

# All @register() are a product of reviewing Yaksha
# See utilities.register for more information

@register('help-nog')
async def help(command, msg, user, channel, *args, **kwargs):
    return "For more information about the bot and its commands: https://github.com/lizardman301/Lizard-bot-rsf"

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

@register('get-users')
async def get_users(command, msg, user, channel, *args, **kwargs):
    users = kwargs['full_msg'].guild.members
    userList = {}

    for user in users:
        userList.update({user.name + '#' + str(user.discriminator): user.display_name})

    return userList