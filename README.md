# Lizard-BOT

Simple discord bot originally built for the r/streetfighter East Coast online weekly tournament to help players see current round and with some commands for TOs. Support for multiple channels to run multiple tournaments at once and allows for custom prefixes, round flavor text, and more. Requires discord.py and pymysql.

# How to Use

In order to get started, you need to invite NogBot-Utils to the discord server you wish to use to run tournaments.  Invite link coming soon.

Immediately after the bot joins the server use the command `$edit botrole <role>` with the role of your choice to make it so that only those with that role can access the commands meant for the Tournament Organizers. From there, feel free to use all the commands listed below to adjust the bot to your needs.

## TO Commands

These commands will only be available to be used by those with the role mentioned above.

`$botrole`
Returns the role that allows access to the administrator commands.

`$edit <setting> <value>`

There are multiple settings that can be edited to allow customization.

##### Server-wide
 * botrole
	 * This role determines what role is needed to access the TO Commands
	 * New value must be a ping to the role desired
	 * Default value: @everyone
 * prefix-nog
	 * Allows you to change the prefix for commands
	 * Useful if you use multiple bots that may have similar commands and prefixes
	 * Default Value: $

`$prefix-nog`
Prints the prefix currently in use for NogBot-Utils.

## General commands
Commands everyone can use

`$help-nog`
Links back to this page.

`$ping-nog`
Ping! Pong!

## Contributers
* **Nogarremi** - *Database implentation* - [Twitter](https://twitter.com/Nogarremi)
* **Lizardman** - *Initial work, owner of bot, bug hunting* - [Twitter](https://twitter.com/lizardman301)
* **Axio** - *Initial Idea and general help*

## Other Resources
* **[Yaksha Bot](https://github.com/ellipses/Yaksha)** - *Created by ellipses. We used this for additional ideas about proper structuring of code for ease of expandability and readability. Yaksha Bot was released under an MIT license and this bot(Lizard-bot-rsf) is re-released as Mozilla Public License 2.0 but to ensure ellipses is credited, the functions copied and then edited by the contributors are commented with "# Yaksha" to give credit*