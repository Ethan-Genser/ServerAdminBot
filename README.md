# ServerAdminBot
Discord bot that allows users to manage a Minecraft server remotely

## Prerequisites

Before you can run this program, ensure that you have the following software installed and functional:
* An instance of a vanilla Minecraft server
* Python 3.7 or later
* The following python packages: discord, psutil
* Note: This program is designed to be run inside the Windows operating system

## Installation
1. Vist the [Discord Developer Portal](https://discord.com/developers/applications) and create a new application.
2. Under the Bot tab in the new Discord application, add a new bot.
3. Under the OAuth2 tab in the Discord application set the scope to "bot" and make sure the bot permissions allow it to send messages and use external emojis.
4. Copy the URL above the permissions box and paste it into a new tab on your browser. This will allow you to invite the new bot to your Discord server. (note: you will need admin permissions on the server to invite a new bot.)
5. Back in the Bot tab copy the bot's authentication token. Then add a new enviroment variable to your Windows OS named "DISCORD_TOKEN" (without the quotation marks). Set the value of this variable by pasting the bot's authentication token. 
6. Use pip to install the python packages listed in the Prerequisites section of this file.
7. Finally, download the source code from this repository and copy the contents into your Minecraft server's root folder.
8. You should now be ready to start your bot by following the procedure outlined in the Running section of this file!

## Running
1. Start the Discord bot by running [__startbot.bat__](startbot.bat)
2. The program should create a new window and, after signing in with the authentication token, display "Logged in as \<BotName\>".
3. You are now ready to start sending the bot commands from any Discord server where the bot has been added! For a list of currently implemented commands use the command "/help" (without the quotation marks).

## Authors
* [**Ethan Genser**](https://github.com/Ethan-Genser) - *Creator*
