import re
import pymysql.cursors # Use for DB connections
from secret import sql_host,sql_port,sql_user,sql_pw,sql_db # Store secret information

_callbacks = {}

# Yaksha
def register(command):
    '''
    _Registers_ each function with by storing the command its name
    into a dict.
    '''
    def decorator(func):
        print('Registering %s with command %s' % (func.__name__, command))
        _callbacks[command] = (func.__qualname__, func.__module__)
        return func
    return decorator

# Yaksha
def get_callbacks():
    '''
    Simple getter that returns the dictionary containing
    the registered functions. Might be better to make
    registration into a class instead.
    '''
    return _callbacks

# Add Markdown for bold
def bold(string):
    return "**" + string + "**"

def pings_b_gone(list):
    #for the list passed, it will return a list with any pings replaced with text of the ping instead
    reg = re.compile('<@(!|&)\d*>')

    for i, x in enumerate(list):
        if reg.fullmatch(x):
            list [i] = x[3:][:-1]

    #return new list with now pings
    return list

# Create a connection to the database
def make_conn():
    return pymysql.connect(host=sql_host, port=sql_port, user=sql_user, password=sql_pw, db=sql_db, charset='utf8mb4', autocommit=True, cursorclass=pymysql.cursors.DictCursor)

# Check if the guild/channel is in the table
# If not, add it the guilds, channels, and settings tables
def settings_exist(guild_id, chan_id):
    conn = make_conn() # Make DB connection

    try:
        with conn.cursor() as cursor:
            for level in ['guild','channel']:
                ids = [] # Store a list of all ids
                id = guild_id if level == 'guild' else chan_id # Set variable id based on what level of setting

                # Select all IDs in the DB for the given level
                sql = "SELECT " + level + "_id FROM " + level + "s"
                cursor.execute(sql)
                for row in cursor:
                    ids.append(row[level + '_id']) # Add IDs to the list

                # If the ID is not in the list
                # Add the ID to the guild/channel table
                # Add the ID to the guild/channel_settings table (This will initialize the default values)
                if id not in ids:
                    sql = "INSERT INTO " + level + "s (" + level + "_id) VALUES (%s)"
                    cursor.execute(sql, (id,))
                    
                    sql = "INSERT INTO " + level + "_settings (" + level + "_id) VALUES (%s)"
                    cursor.execute(sql, (id,))
    finally:
        conn.close() # Close the connection

    return 1 # Return truthy value for checking

# Read a setting from database for a given guild/channel
def read_db(level, setting, id):
    conn = make_conn() # Make DB Connection

    try:
        with conn.cursor() as cursor:
            # Select the desired setting from the DB for the given guild/channel
            sql = "SELECT `" + setting + "` FROM " + level + "_settings WHERE " + level + "_id = %s"
            cursor.execute(sql, (id))
            return cursor.fetchone()[setting] # Return the value for the setting
    finally:
        conn.close() # Close the connection

# Save a setting for a given guild/channel to the database
def save_db(level, setting, data, id, **kwargs):
    conn = make_conn() # Make DB Connection

    try:
        with conn.cursor() as cursor:
            # Update the desired setting in the DB for the given guild/channel
            if kwargs:
                id = kwargs['commandChannel']
            sql = "UPDATE " + level + "_settings SET `" + setting + "` = %s WHERE " + level + "_id = %s"
            cursor.execute(sql, (data, id))
    finally:
        conn.close() # Close the connection