# -*- coding: utf-8 -*-

import random as randomlib

def random(args):
	min = int(float(args[1]))
	max = int(float(args[2]))

	usage = '!random <min> <max>'

	try:
		return randomlib.randint(min, max)
	except IndexError:
		return '!random <min> <max> (use full integers)'
	except:
		return usage