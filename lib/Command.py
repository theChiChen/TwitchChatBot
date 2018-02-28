# -*- coding: utf-8 -*-

import importlib
from commands.CommandList import *

class Commandlib(object):

	def __init__(self):
		super(Commandlib, self).__init__()

	def is_valid_command(self, command):
		if command in commands:
			return True

	def check_has_return(self, command):
		if commands[command]['return'] and commands[command]['return'] != 'command':
			return True

	def get_return(self, command):
		return commands[command]['return']

	def check_returns_function(self, command):
		if commands[command]['return'] == 'command': 
			return True  

	def get_return(self, command):
		return commands[command]['return']

	def check_has_correct_args(self, command, arguments):
		if len(arguments) - 1 == commands[command]['argc']:
			return True

	def pass_to_function(self, command, args):
		command = command.replace('!', '')
	
		module = importlib.import_module('commands.%s' % command)
		function = getattr(module, command)
	
		if args:
			return function(args)
		else:
			return function()