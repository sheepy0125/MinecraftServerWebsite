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
from datetime import datetime, time as dt_time
from json import load, dump
from requests import post

with open("json_files/config.json") as config_file:
	config_dict = load(config_file)
	LOOP_INTERVAL = config_dict["loopInterval"]
	SERVER_LOCAL_IP = config_dict["serverLocalIP"]
	EXTERNAL_IP = config_dict["publicIP"]
	ANOMALY_WEBHOOK_URL = config_dict["anomalyWebhookURL"]

SERVER = MinecraftServer.lookup(f"{EXTERNAL_IP}:25565")
SERVER_LOCAL = MinecraftServer.lookup(f"{SERVER_LOCAL_IP}:25565")

# Ping anomaly
def ping_anomaly(message_to_send):
	data_to_send = {
		"username": "Anomaly detector bot",
		"content": f"{message_to_send}"
	}
	post(ANOMALY_WEBHOOK_URL, json=data_to_send, headers={
		"Content-Type": "application/json"}).raise_for_status()

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
			players_left = 0 # This is for checking if a bunch of players left
			for player in list(players_online_dict.keys()):
				if player not in players_online:
					players_left += 1
					del players_online_dict[player]
			
			# Anomaly detection
			if players_left >= 2:
				ping_anomaly(message_to_send=f"Two or more players left at once. ({players_left}), but the external connection is up.")

		except ConnectionError:
			# Server is offline

			# If it has just gone offline (it's still set as up)
			if server_status_dict["serverUp"]:
				# Set the files to be offline for the first time
				server_status_dict["serverUp"] = False
				server_status_dict["firstPingTime"] = 0
				server_status_dict["lastPingTime"] = current_time
				players_online_dict = {}

				# Send anomaly if it is not just restarting (restarts at 5 A.M.)
				min_time = dt_time(4, 55, 0) # 4:55 A.M.
				max_time = dt_time(5, 5, 0) # 5:05 A.M.
				
				if not (max_time >= datetime.now().time() >= min_time): # Returns True if the current time is inbetween the min_time and max_time
					# Check if it's just the external connections
					try:
						SERVER_LOCAL.ping()
						message_to_send = "The external connection to the server has gone down!!! @everyone"
					except ConnectionError:
						message_to_send = "The server has gone down!!! @everyone"
					# Send anomaly
					ping_anomaly(message_to_send=message_to_send)
			
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