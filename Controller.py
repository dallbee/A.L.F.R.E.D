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

	def sync(self):
		print("[SEND]")
		for i, irc in enumerate(self.irc):
			irc.send(bytes(self.tx[i], self.settings["encoding"]))
			print(self.tx[i])
			self.tx[i] = ""

		print("[RECV]")
		for i, irc in enumerate(self.irc):
			end = False
			rx_buffer = []
			while (not end):
				received = irc.recv(self.settings["buffer_size"]).decode(self.settings["encoding"])
				rx_buffer.append(received)
				if (not received or received[-2:] == "\r\n"):
					end = True

			self.rx[i] = "".join(rx_buffer)
			print(self.rx[i])

	def read(self):
		read_buffer = []
		for i, connection in enumerate(self.connections):
			read_buffer.append(self.rx[i].split('\n'))
			self.rx[i] = ""

		return read_buffer

	def write(self, connection, message):
		self.tx[connection] = "".join([self.tx[connection], message, "\r\n"])






