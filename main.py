#!/usr/bin/python3
import time
from Controller import *

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
		"channels": {"##XAMPP"},
	},
]

settings = {
	"encoding": "UTF-8",
	"sync_frequency": 10,
	"buffer_size": 4096,
}

last_sync = 0
read_buffer = []
IRC = Controller(connections, identity, settings)

while True:
	read_buffer = IRC.read()

	for i, connection in enumerate(connections):
		for line in read_buffer[i]:
			if (line[:4] == "PING"):
				IRC.write(i, "PONG{0}".format(line[4:]))
			if (line.find("PRIVMSG ##XAMPP :AllBot") != -1):
				IRC.write(i, "PRIVMSG ##XAMPP :Sorry, I'm not ready to respond to you!")
	
	if (time.clock() - last_sync > 1/settings["sync_frequency"]):
		IRC.sync()
		last_sync = time.clock()
