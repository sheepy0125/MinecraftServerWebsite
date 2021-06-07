"""
Discord bot for Minecraft Server Website
Created on 06/06/2021 (June 6th, 2021)
Last updated on 06

This depends on `api.py` being up.
"""

""" Setup """

from discord import Embed, Game
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from json import load
from requests import get

client = commands.Bot(command_prefix="\\", case_insensitive=True)
client.remove_command("help")
slash = SlashCommand(client, sync_commands=True)

with open("json_files/config.json") as config_file:
	config_dict = load(config_file)
	# API_URL = f"http://{config_dict['publicIP']}:{config_dict['websitePort']}"
	API_URL = "http://127.0.0.1:3000"
	LOG_FILE_LOCATION = config_dict["logFileLocation"]
	ADMIN_USERS = config_dict["adminUserIDs"]
	BOT_TOKEN = config_dict["botToken"]

""" Events """

# Bot startup
@client.event
async def on_ready():
	print("The Discord bot is ready now!")
	await client.change_presence(activity = Game("/help"))

# Error handler
@client.event
async def on_slash_command_error(ctx: SlashContext, exception):
	await ctx.send(f"""
An error has occured!!! 
> {'Error with fetching data from the API, is it up?' if str(exception) == 'Expecting value: line 1 column 1 (char 0)' else str(exception)}
	""")

""" Commands """

# Help
@slash.slash(name="help")
async def _help_command(ctx: SlashContext):
	with open("json_files/bot_docs.json") as bot_docs_file:
		bot_docs_dict = load(bot_docs_file)

		# Help embed
		help_embed = Embed(title="List of commands", color=0xff80ff)
		for command in bot_docs_dict.keys():
			help_embed.add_field(name=command, value=bot_docs_dict[command], inline=False)

		await ctx.send(embed=help_embed)

# Ping
@slash.slash(name="ping")
async def _ping_command(ctx: SlashContext):
	try:
		(get(f"{API_URL}/ping").json())["worked"]
		await ctx.send("Pong!")
	except Exception: # This should only be KeyError and JSONDecodeError, but I can't use the latter
		await ctx.send("The API is down!!!")
	

# Status
@slash.slash(name="status")
async def _status_command(ctx: SlashContext):
	# Get the status and players online
	server_status = (get(f"{API_URL}/get_server_status").json())["information"]
	players_online = (get(f"{API_URL}/get_players_online_information").json())["player_informations"]

	# Create an embed
	status_embed = Embed(color=0xff80ff)
	status_embed.add_field(
		name=f"Server status.", 
		value=f"``The server is currently {'up' if server_status['serverUp'] else 'down'} and has has been for {server_status['timeFormatted']}``",
		inline=False
	)

	# Display players who are online if the server is up
	if server_status["serverUp"]:
		players_online_text = ""
		player_count = 0
		for player in players_online.keys():
			player_count += 1
			players_online_text += f"``{player} - {players_online[player]['timeFormatted']} played``\n"

		status_embed.add_field(
			name=f"Players online",
			value=f"""
				``There {'are' if player_count != 1 else 'is'} {player_count} player{'s' if player_count != 1 else ''} online.``
				{players_online_text}
			""",
			inline=False
		)
	
	await ctx.send(embed=status_embed)

# Whitelist
@slash.slash(name="whitelist")
async def _whitelist_command(ctx: SlashContext):
	# Get the players that are whitelisted
	players_whitelisted = (get(f"{API_URL}/get_whitelisted_players").json())["players"]
	
	# Create an embed
	whitelist_embed = Embed(color=0xff80ff)

	# Display all the players who are whitelisted
	players_whitelisted_text = ""
	player_id = 0
	for player in players_whitelisted:
		player_id += 1
		players_whitelisted_text += f"{str(player_id).zfill(2)}{player:>18}\n"

	whitelist_embed.add_field(
		name="Players whitelisted",
		value=f"```{players_whitelisted_text}```",
		inline=False
	)

	await ctx.send(content="Want to add someone? Contact sheepy!", embed=whitelist_embed)

# Website
@slash.slash(name="website")
async def _website_command(ctx: SlashContext):
	await ctx.send(f"The website is at {API_URL}.")

# Get log
@slash.slash(name="get_log")
async def _get_log(ctx: SlashContext, lines: str):
	# Make sure only admin users can use this
	if ctx.author_id not in ADMIN_USERS:
		await ctx.send("This is a protected command. You must be an admin to use it.")
		return

	lines_number: int = int(lines)

	with open(LOG_FILE_LOCATION) as log_file:
		# Get all lines of the file
		log_lines = log_file.readlines()

		# If lines_number is too high, just set it to the maximum amount.
		if lines_number > (len(log_lines)):
			lines_number = (len(log_lines))

		# Get the lines
		needed_lines = log_lines[(len(log_lines) - lines_number):(len(log_lines))]

		# Make the lines pretty
		needed_lines_output = ""
		line_number = 0
		for line in needed_lines:
			line = line.strip("\n") # Remove the \n so it prints properly.
			line_number += 1
			needed_lines_output += f"Line {str(line_number).zfill(3)}: {line}\n"

	# Split the output into 1,900 character chunks (not 2,000 so it can be wrapped in ```)
	for char_idx in range(0, len(needed_lines_output), 1900):
		await ctx.send(f"```\n{needed_lines_output[char_idx:(char_idx + 1900)]}```")

""" Run """

if __name__ == "__main__":
	client.run(BOT_TOKEN)