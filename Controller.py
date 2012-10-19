#!/usr/bin/python3
import socket
import string

class Controller:
	connections = []
	identity = {}
	settings = {}

	irc = []
	rx = []
	tx = []

	def __init__(self, connections, identity, settings):
		self.connections = connections
		self.identity = identity
		self.settings = settings
		self._connect()

	def _connect(self):
		for i, connection in enumerate(self.connections):
			self.rx.append("")
			self.tx.append("")
			self.irc.append(socket.socket())
			self.irc[i].connect((connection["server"], connection["port"]))
			self.write(i, "NICK {0}".format(self.identity["nick"]))
			self.write(i, "USER {0} * * :{1}".format(self.identity["user"], self.identity["real"]))
			for channel in connection["channels"]:
				self.join(i, channel)

	def join(self, connection, channel):
		self.write(connection, "JOIN {0}".format(channel))

	def leave(self, connection, channel):
		self.write(connection, "LEAVE {0}".format(channel))

	def sync(self):
		print("[SEND]")
		for i, irc in enumerate(self.irc):
			irc.send(bytes(self.tx[i], self.settings["encoding"]))
			print(self.tx[i])
			self.tx[i] = ""

		print("[RECV]")
		for i, irc in enumerate(self.irc):
			self.rx[i] = irc.recv(self.settings["buffer_size"]).decode(self.settings["encoding"])
			print(self.rx[i])

	def read(self):
		read_buffer = []
		for i, connection in enumerate(self.connections):
			read_buffer.append(self.rx[i].split('\n'))
			self.rx[i] = "0"

		return read_buffer

	def write(self, connection, message):
		self.tx[connection] = ''.join([self.tx[connection], message, "\r\n"])






