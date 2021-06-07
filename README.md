# Minecraft Server Website

Well, this is a website and a Discord bot mashed together with the same API.
[Video showing it](https://www.youtube.com/watch?v=nEpJCIa_GQE)

File tree:
├── README.md
├── api
│	├── api.py
│	├── bot.py
│	├── json_files
│	│	├── api_docs.json
│	│	├── bot_docs.json
│	│	├── config.json (hidden)
│	│	├── connection_instructions.json (hidden)
│	│	├── players_online_information.json (hidden)
│	│	├── rules.json (hidden)
│	│	├── server_status_information.json (hidden)
│	│	└── whitelisted_players.json (hidden)
│	├── status_loop.py
│	|── template
│	|	└── index.html
|	└── venv (hidden)
├── craco.config.js
├── package-lock.json (hidden)
├── package.json
├── postcss.config.js
├── public
│	└── index.html
├── src
│	├── components
│	│	├── connectionInstructions.jsx
│	│	├── contact.jsx
│	│	├── main.jsx
│	│	├── pingServer.jsx
│	│	├── playersOnline.jsx
│	│	├── rules.jsx
│	│	├── serverStatus.jsx
│	│	└── whitelistedPlayers.jsx
│	├── index.css
│	└── index.js
├── tailwind.config.js
└── yarn.lock (hidden)