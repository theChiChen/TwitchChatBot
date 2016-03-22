# -*- coding: utf-8 -*-
import socket, sys, time, errno, re, select
import Config


class Bot(object):

	def __init__(self):
		try:
			self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		except socket.error as e:
			print(e)
			sys.exit(1)

	def _connect(self):
		try:
			self.socket.connect((Config.server, Config.port))
		except socket.error as e:
			print(e)
			sys.exit(1)

	def _login(self):
		try:
			self.socket.send(("PASS %s\n\r" % Config.oauth_password).encode("utf-8"))
			self.socket.send(("NICK %s\n\r" % Config.nick).encode("utf-8"))
		except socket.error as e:
			print(e)
			sys.exit(1)

		if self._check_login_status(self.receive_socket_data()):
			print('[%s] Login "%s" successful.' % (time.strftime('%H:%M:%S', time.localtime()), Config.nick))
			return True
		else:
			print('[%s] Login "%s" unsuccessful. (hint: make sure your oauth token is set in Config.py).' % (time.strftime('%H:%M:%S', time.gmtime()), Config.nick))
			sys.exit(1)

	def _check_login_status(self, data):
		if re.match(r'^:tmi\.twitch\.tv NOTICE \* :Login unsuccessful$', data):
			return False
		elif re.match(r'^:tmi\.twitch\.tv NOTICE \* :Error logging in$', data):
			return False
		else:
			return True
		
	def _join(self):
		try:
			self.socket.send(("JOIN #%s\n\r" % Config.channel).encode("utf-8"))
		except socket.error as e:
			print(e)
			sys.exit(1)
		timeout = time.time() + 20   # 20 sec from now
		while True:
			connected = self._check_join_status(self.receive_socket_data())
			if connected:
				return True
			elif time.time() > timeout:
				sys.exit(1)

	def _check_join_status(self, line):
		if("End of /NAMES list" in line):
			print('[%s] Join channel "#%s" successful.' % (time.strftime('%H:%M:%S', time.localtime()), Config.channel))
			return True
		else:
			return False

	def receive_socket_data(self):
		readable, writable, exceptional = select.select([self.socket], [], [], 1)
		for sock in readable:
			if sock == self.socket:
				socket_data = self.socket.recv(Config.socket_buffer_size).decode("utf-8", "ignore")
				if len(socket_data) == 0:
					print('[%s][%s][Error] Connection was lost.' % (time.strftime('%H:%M:%S', time.localtime()), Config.channel))
					sys.exit(1)
				return socket_data
		return None

	def get_socket(self):
		self._connect()
		if not self._login():
			sys.exit(1)
		if not self._join():
			sys.exit(1)
		self.socket.send(("PRIVMSG #%s :%s\r\n" % (Config.channel, Config.welcome_message)).encode("utf-8"))
		print('[%s][#%s][Login] %s' % (time.strftime('%H:%M:%S', time.localtime()), Config.channel, Config.welcome_message))
		return self.socket