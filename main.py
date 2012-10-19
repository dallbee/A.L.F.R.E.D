#!/usr/bin/python3
import time
from Controller import *
from Alfred import *

identity = {
	"nick": "Alfred",
	"user": "Alfred",
	"real": "Alfred IRCBot",
}

connections = [
	{
		"server": "irc.freenode.net",
		"port": 6667,
		"ssl": False,
		"channels": ["##XAMPP"],
	},
]

settings = {
	"encoding": "ASCII",
	"sync_frequency": 10,
	"buffer_size": 2048,
}

last_sync = 0
read_buffer = []
irc = Controller(connections, identity, settings)
bot = []

for connection in connections:
	bot.append(Alfred(identity, connection["channels"]))

while True:
	read_buffer = irc.read()

	for i, connection in enumerate(connections):
		for line in read_buffer[i]:
			bot[i].parse(line)
			for response in bot[i].response():
				irc.write(i, response)
	
	if (time.clock() - last_sync > 1/settings["sync_frequency"]):
		irc.sync()
		last_sync = time.clock()
