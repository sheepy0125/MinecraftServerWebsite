"""
API for Minecraft Server Website
Created on 06/04/2021 (June 4th, 2021)
"""

""" Setup """

from flask import Flask, config, render_template, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from time import time
from json import load
from requests import post

api: object = Flask(__name__, template_folder="template")
api.config["TRAP_HTTP_EXCEPTIONS"] = True
limiter: object = Limiter(api, key_func=get_remote_address)

with open("json_files/config.json") as config_file:
	config_dict = load(config_file)
	WEBHOOK_URL = config_dict["webhookURL"]
	PUBLIC_IP_ADDRESS = config_dict["publicIP"]

""" Routes """

# Root page
@api.route("/")
@limiter.limit("1 per 10 second")
def root_page_route() -> str:
	with open("json_files/api_docs.json") as docs_file:
		return render_template("index.html", route_docs=load(docs_file))

# Ping
@api.route("/ping")
def ping_route() -> dict:
	return {"worked": True}

# Get information for the players who are online
@api.route("/get_players_online_information")
@limiter.limit("1 per second")
def get_players_online_route() -> dict:
	with open("json_files/players_online_information.json") as players_online_information_file:
		return {"worked": True, "player_informations": load(players_online_information_file)}

# Get server status
@api.route("/get_server_status")
@limiter.limit("1 per second")
def get_server_status_route() -> dict:
	with open("json_files/server_status_information.json") as server_status_information_file:
		return {"worked": True, "information": load(server_status_information_file)}

# Get whitelisted players
@api.route("/get_whitelisted_players")
@limiter.limit("1 per 3 second")
def get_whitelisted_players_route() -> dict:
	with open("json_files/whitelisted_players.json") as whitelisted_players_file:
		return {"worked": True, "players": load(whitelisted_players_file)}

# Get rules
@api.route("/get_rules")
@limiter.limit("1 per second")
def get_rules_route() -> dict:
	with open("json_files/rules.json") as rules_file:
		return {"worked": True, "rules": load(rules_file)}

# Get connection instructions
@api.route("/get_connection_instructions")
@limiter.limit("1 per second")
def get_connection_instructions_route() -> dict:
	with open("json_files/connection_instructions.json") as connection_instructions_file:
		connection_instructions_dict: dict = load(connection_instructions_file)
		return {"worked": True, "instructions": connection_instructions_dict["instructions"], "ip_address": connection_instructions_dict["ipAddress"]}

# Get other links
@api.route("/get_other_links")
@limiter.limit("1 per second")
def get_other_links_route() -> dict:
	with open("json_files/other_links.json") as other_links_file:
		return {"worked": True, "links": load(other_links_file)}

# Contact Pink_Sheepy
@api.route("/contact_sheepy", methods=["POST"])
@limiter.limit("1 per 3 minute")
def contact_sheepy_route() -> dict:
	username = request.json["username"]
	message = request.json["message"]

	# Send a Discord Webhook
	data_to_send = {
		"username": username,
		"content": f"{message} \n\nSent at {time()}. Ping: <@!246795601709105153>"
	}
	post(WEBHOOK_URL, json=data_to_send, headers={
		"Content-Type": "application/json"}).raise_for_status()

	return {"worked": True}


""" Error handlers """

# All error handlers
@api.errorhandler(Exception)
def error_handler(error):
	try:
		# HTTP error code (error.code works)
		return {"worked": False, "message": "An HTTP exception has occured.", "error_message": str(error), "error_code": error.code}
	except Exception:
		# Internal error
		return {"worked": False, "message": "An internal exception has occurred.", "error_message": str(error)}
