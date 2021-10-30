import discord
import os
import psutil
import subprocess
import time

# Checks if the given process is currently running on this machine
def checkIfProcessRunning(processName):
	# Iterate over the all the running process
	for proc in psutil.process_iter():
		try:
			# Check if process name contains the given name string
			if proc.name().lower() == processName.lower():
				return True
		except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
			pass
	return False

# Starts the given process
def startProcess(processName):
	if (not checkIfProcessRunning(server)):
		subprocess.Popen('startserver-nogui.bat')
		return True
	else:
		return False

# Kills the given process
def killProcess(processName):
	if (checkIfProcessRunning(processName)):
		# Iterate over the all the running process
		for proc in psutil.process_iter():
			try:
				# check whether the process name matches
				if proc.name().lower() == processName:
					proc.kill()
					return True
			except:
				pass
		return False
	else:
		return False

server = 'java.exe'
client = discord.Client()

# Discord client event listeners
@client.event
async def on_ready():
	print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
	if (message.author == client.user):
		return

	msg = message.content

	# Say hello to the bot :)
	if (msg.startswith('/hello')):
		print ('command received: /hello')
		await message.channel.send('Hello!')

	
	# Say hello to the bot :)
	if (msg.startswith('/help')):
		print ('command received: /help')
		await message.channel.send('/hello:     Hi!')
		await message.channel.send('/status:   Shows the current status of the server.')
		await message.channel.send('/start:     Starts the server.')
		await message.channel.send('/stop:      Stops the server.')
		await message.channel.send('/restart:  Restarts the server.')


	# Check the status of the server
	if (msg.startswith('/status')):
		print ('command received: /status')
		if (checkIfProcessRunning(server)):
			await message.channel.send('Server Status: Running :white_check_mark:')
			await message.channel.send('CPU:          ' + str(psutil.cpu_percent()) + '%')
			await message.channel.send('RAM:         ' + str(psutil.virtual_memory().percent) + '%')
		else:
			await message.channel.send('Server Status: Not Running :x:')
			await message.channel.send('Pro Tip: If you would like to start the server use the /start command.')

	
	# Start the server
	if (msg.startswith('/start')):
		print ('command received: /start')
		if (startProcess(server)):
			await message.channel.send('Starting server... One moment please.')
			time.sleep(15)
			await message.channel.send('Server Status: Running :white_check_mark:')
		else:
			await message.channel.send('Server is already running!')
		

	
	# Stop the server
	if (msg.startswith('/stop')):
		print ('command received: /stop')
		if (killProcess(server)):
			await message.channel.send('Server stopped.')
		else:
			await message.channel.send('Server is not running.')
	


	# Restart the server
	if (msg.startswith('/restart')):
		print ('command received: /restart')
		if (killProcess(server)):
			await message.channel.send('Stopping server...')
			if (startProcess(server)):
				await message.channel.send('Restarting server...')
				time.sleep(15)
				await message.channel.send('Server Status: Running :white_check_mark:')
			else:
				await message.channel.send('Failed to restart server! Contact an admin for help.')
		else:
			await message.channel.send('Server is not running.')


# Run discord client
client.run(os.getenv('DISCORD_TOKEN'))