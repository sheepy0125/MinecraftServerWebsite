"""
API for Minecraft Server Website
Created on 06/06/2021 (June 6th, 2021)

This is for setting the following files with up-to-date information:
server_status_information.json
players_online_information.json
"""

""" Setup """

from mcstatus import MinecraftServer
from time import time, sleep, gmtime, strftime
from json import load, dump

with open("json_files/config.json") as config_file:
	config_dict = load(config_file)
	LOOP_INTERVAL = config_dict["loopInterval"]
	SERVER_LOCAL_IP = config_dict["serverLocalIP"]
	

SERVER = MinecraftServer.lookup(f"{SERVER_LOCAL_IP}:25565")

""" Loop """	
# Repeat forever
while True:
	# Open the information files
	with open("json_files/players_online_information.json", "r+") as players_online_information_file, \
		open("json_files/server_status_information.json", "r+") as server_status_information_file:
		# Get the current time
		current_time = int(time())

		# Load the files
		players_online_dict = load(players_online_information_file)
		server_status_dict = load(server_status_information_file)

		# Get the server status
		try: 
			SERVER.ping()

			# Server is online

			# If it has just gone online (it's still set as down)
			if not server_status_dict["serverUp"]:
				# Set the files to be online for the first time
				server_status_dict["serverUp"] = True
				server_status_dict["firstPingTime"] = current_time
				server_status_dict["lastPingTime"] = current_time

			# Get the players online
			players_online = SERVER.query().players.names

			# For every player online, update the file
			for player in players_online:
				# Check if the player was already created
				if player not in list(players_online_dict.keys()):
					# Create the player
					players_online_dict[player] = {"joinTime": current_time, "time": 0}

				# Update player time
				players_online_dict[player]["time"] = (current_time - players_online_dict[player]["joinTime"])
				players_online_dict[player]["timeFormatted"] = strftime("%H hours %M minutes %S seconds", gmtime(players_online_dict[player]["time"]))

			# Delete extra players
			for player in list(players_online_dict.keys()):
				if player not in players_online:
					del players_online_dict[player]

		except ConnectionRefusedError:
			# Server is offline

			# If it has just gone offline (it's still set as up)
			if server_status_dict["serverUp"]:
				# Set the files to be offline for the first time
				server_status_dict["serverUp"] = False
				server_status_dict["firstPingTime"] = 0
				server_status_dict["lastPingTime"] = current_time
				players_online_dict = {}
			
		# Set server uptime/downtime

		if server_status_dict["serverUp"]:
			# Uptime
			server_status_dict["time"] = (current_time - server_status_dict["firstPingTime"])
		else:
			# Downtime
			server_status_dict["time"] = (current_time - server_status_dict["lastPingTime"])

		# Set the time formatted (fromtimestamp turns the UNIX timestamp into a datetime.datetime object)
		server_status_dict["timeFormatted"] = strftime("%H hours %M minutes %S seconds", gmtime(server_status_dict["time"]))

		# Save
		players_online_information_file.truncate(0)
		players_online_information_file.seek(0)
		server_status_information_file.truncate(0)
		server_status_information_file.seek(0)
		dump(players_online_dict, players_online_information_file, indent=4)
		dump(server_status_dict, server_status_information_file, indent=4)

		print(server_status_dict)
		print(players_online_dict)

	sleep(LOOP_INTERVAL)