#!/usr/bin/python3
import string

class Alfred:

	response_buffer = []

	def __init__(self, identity, channels = []):
		for channel in channels:
			self.join(channel)


	def parse(self, line):
		if (line[0:4] == "PING"):
			self.ping(line[:5])
			return True
		if (line.find(":") != 0):
			return False

		line = line.split(":", 2)[1:]

		if (len(line) < 2):
			return False

		parameters = line[0].split(" ")
		nick = parameters[0].split("!", 0)
		message = line[1]

		if (parameters[1] == "PRIVMSG"):
			self.message(message)

	def response(self):
		response = self.response_buffer
		self.response_buffer = []
		return response

	def ping(self, host):
		self.response_buffer.append("PONG")

	def join(self, channel):
		self.response_buffer.append("JOIN {0}".format(channel))

	def leave(self, channel):
		self.response_buffer.append("LEAVE {0}".format(channel))

	def message(self, message):
		if (message[:3] == "SAY"):
			self.response_buffer.append("".join(["PRIVMSG ##XAMPP :", message[4:]]))
