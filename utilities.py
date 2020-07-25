import pymysql.cursors # Use for DB connections
from secret import sql_host,sql_port,sql_user,sql_pw,sql_database # Store secret information

_callbacks = {} # Yaksha

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

def get_users(msg):
    users = msg.guild.members
    userDict = {}

    for user in users:
        userDict.update({user.name + '#' + str(user.discriminator): user.display_name.lower()})

    return userDict

# Create a connection to the database
def make_conn():
    return pymysql.connect(host=sql_host, port=sql_port, user=sql_user, password=sql_pw, db=sql_database, charset='utf8mb4', autocommit=True, cursorclass=pymysql.cursors.DictCursor)

# Check if the guild/channel is in the table
# If not, add it the guilds, channels, and settings tables
def settings_exist(guild_id):
    conn = make_conn() # Make DB connection

    try:
        with conn.cursor() as cursor:
                guilds = []

                # Select all IDs in the DB for the given level
                sql = "SELECT guild_id FROM guilds"
                cursor.execute(sql)
                for row in cursor:
                    guilds.append(row['guild_id']) # Add IDs to the list

                # If the ID is not in the list
                # Add the ID to the guild/channel table
                # Add the ID to the guild/channel_settings table (This will initialize the default values)
                if guild_id not in guilds:
                    sql = "INSERT INTO guilds (guild_id) VALUES (%s)"
                    cursor.execute(sql, (guild_id,))

                    sql = "INSERT INTO guild_settings (guild_id) VALUES (%s)"
                    cursor.execute(sql, (guild_id,))
    except Exception:
        return 0 # Falsy value to fail
    finally:
        conn.close() # Close the connection

    return 1 # Return truthy value for checking

# Read a setting from database for a given guild/channel
def read_db(setting, id):
    conn = make_conn() # Make DB Connection

    try:
        with conn.cursor() as cursor:
            # Select the desired setting from the DB for the given guild/channel
            sql = "SELECT `" + setting + "` FROM guild_settings WHERE guild_id = %s"
            cursor.execute(sql, (id))
            return cursor.fetchone()[setting] # Return the value for the setting
    finally:
        conn.close() # Close the connection

# Save a setting for a given guild/channel to the database
def save_db(setting, data, id, **kwargs):
    conn = make_conn() # Make DB Connection

    try:
        with conn.cursor() as cursor:
            # Update the desired setting in the DB for the given guild/channel
            if kwargs:
                id = kwargs['commandChannel']
            sql = "UPDATE guild_settings SET `" + setting + "` = %s WHERE guild_id = %s"
            cursor.execute(sql, (data, id))
    finally:
        conn.close() # Close the connection