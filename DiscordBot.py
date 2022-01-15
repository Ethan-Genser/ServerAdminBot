import discord
import os
import glob
import psutil
import shutil
import subprocess
import time
import atexit

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
		subprocess.Popen(processName)
		return True
	else:
		return False

# Kills the given process
def killProcess(processName):
	ret = False
	if (checkIfProcessRunning(processName)):
		# Iterate over the all the running process
		for proc in psutil.process_iter():
			try:
				# check whether the process name matches
				if proc.name().lower() == processName:
					proc.kill()
					ret = True
			except:
				pass
		return ret
	else:
		return ret

# Converts bytes to megabits
def convertToMb(value):
    return value/1024./1024.*8

def bytesToGigabytes(value):
	return value/1024./1024./1024.

# Returns the average network load over a period of time
def getNetworkLoad(seconds):
	avg = 0
	oldValue = 0
	for i in range(0,seconds):
		newValue = psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv
		if (oldValue):
			avg += convertToMb(newValue - oldValue)
		oldValue = newValue
		time.sleep(1)
	return (avg/seconds)
	
# Returns the disk space used by backups and the space remaining
def getArchiveSpace():
	usage = shutil.disk_usage('/')
	return usage
	
# Returns a list of every backup file in the server archive
def getArchive():
	files = glob.glob('/backups/*.zip')
	files = sorted(files, key=os.path.getctime)
	return files
	
# Returns a list of the dates of each backup
def getBackupDates():
	files = getArchive()
	dates = []
	for file in files:
		dates.append(file.split(' ')[1].split('.')[0])
	return dates

# Returns the date of the latest backup
def getLatestBackup():
	dates = getBackupDates()
	latest = dates[len(dates)-1]
	return (latest, os.path.getsize('/backups/backup ' + latest + '.zip'))
	
# Writes to the log file
def log(message):
	print(message)
	# Tries to create a new log file if the current session doesn't already have one
	try:
		open(logPath, 'x')
	except Exception as e:
		pass
	# Tries to open the log file and write the given message
	try:
		with open(logPath, 'a') as f:
			currentTime = time.ctime(time.time()).replace('  ', ' ')
			f.writelines('[' + currentTime + ']    ' + message + '\n')
	except Exception as e:
		print(str(e))


client = discord.Client()
server = 'java.exe'
startServerScript = 'startserver-nogui.bat'
backupScript = 'backup.bat'
startTime = time.ctime(time.time())
logPath = 'logs/DiscordBotLogs/' + startTime.replace(' ', '_').replace(':', '-') + '.txt'
atexit.register(log, message='Client terminated!')

# Discord client event listeners
@client.event
async def on_ready():
	log('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
	if (message.author == client.user):
		return

	msg = message.content

	# Say hello to the bot :)
	if (msg.startswith('/hello')):
		log('command received: /hello')
		await message.channel.send('Hello!')

	
	# Display list of commands and a short description of each one
	if (msg.startswith('/help')):
		log('command received: /help')
		await message.channel.send('/status:    Shows the current status of the server.\n/start:       Starts the server.\n/stop:        Stops the server.\n/restart:    Restarts the server.\n/backup:   Creates a backup of the server.\n/load:         Checks the network load of the server host.\n/archive:   Shows server archive data and history.\n/hello:        Hi!')


	# Check the status of the server
	if (msg.startswith('/status')):
		log('command received: /status')
		if (checkIfProcessRunning(server)):
			await message.channel.send('Server Status: Running :white_check_mark:')
			await message.channel.send('CPU:          ' + str(psutil.cpu_percent()) + '%')
			await message.channel.send('RAM:         ' + str(psutil.virtual_memory().percent) + '%')
		else:
			await message.channel.send('Server Status: Not Running :x:')
			await message.channel.send('Pro Tip: If you would like to start the server use the /start command.')

	
	# Start the server
	if (msg.startswith('/start')):
		log('command received: /start')
		if (startProcess(startServerScript)):
			await message.channel.send('Starting server. One moment please...')
			time.sleep(15)
			await message.channel.send('Server Status: Running :white_check_mark:')
		else:
			await message.channel.send('Server is already running!')
		

	
	# Stop the server
	if (msg.startswith('/stop')):
		log('command received: /stop')
		if (killProcess(server)):
			await message.channel.send('Server stopped.')
		else:
			await message.channel.send('Server is not running.')
	


	# Restart the server
	if (msg.startswith('/restart')):
		log('command received: /restart')
		if (killProcess(server)):
			await message.channel.send('Server Stopped.')
			if (startProcess(server)):
				await message.channel.send('Restarting server. One moment please...')
				time.sleep(15)
				await message.channel.send('Server Status: Running :white_check_mark:')
			else:
				await message.channel.send('Failed to restart server! Contact an admin for help.')
		else:
			await message.channel.send('Server is not running.')


	# Backup the server
	if (msg.startswith('/backup')):
		log('command received: /backup')
		if (not checkIfProcessRunning(server)):
			if (startProcess(backupScript)):
				await message.channel.send('Backing up server. This may take a few minutes...')
				time.sleep(60)
				await message.channel.send('Server backed up!')
			else:
				await message.channel.send('Failed to backup server! Contact an admin for help.')
		else:
			await message.channel.send('I cannot backup the server while it is running.')
	

	# Display current network load
	if (msg.startswith('/load')):
		log('command received: /load')
		if (checkIfProcessRunning(server)):
			await message.channel.send('Checking network load. One moment please...')
			avgBandwidth = getNetworkLoad(10)
			if (avgBandwidth < 4):
				await message.channel.send(':green_circle: Network load is low :green_circle:')
			elif (avgBandwidth < 8):
				await message.channel.send(':yellow_circle: Network load is medium :yellow_circle:')
			else:
				await message.channel.send(':red_circle: Network load is high :red_circle:')
		else:
			await message.channel.send('Server is not running.')

	# Display server archive information
	if (msg.startswith('/archive')):
		log('command received: /archive')
		dates = getBackupDates()
		stringDates = ''
		for date in dates:
			stringDates = stringDates + ':white_small_square:' + date + '\n'
		await message.channel.send('Server backups:\n' + stringDates + '\n:black_small_square:')
		latest = getLatestBackup()
		await message.channel.send(':clock8: Latest backup:     ' + latest[0] + '     ' + str(round(bytesToGigabytes(latest[1]), 2)) + ' GB\n:black_small_square:')
		usage = getArchiveSpace()
		await message.channel.send(':floppy_disk: Disk space used: ' + str(round(bytesToGigabytes(usage.used), 2)) + ' GB\n       Disk space free: ' + str(round(bytesToGigabytes(usage.free), 2)) + ' GB')

# Run discord client
client.run(os.getenv('DISCORD_TOKEN'))