# -*- coding: utf-8 -*-

import random as randomlib

def random(args):

	usage = 'random usage : !random <min> <max> (use full integers)'

	if len(args) == 3:
		min = int(float(args[1]))
		max = int(float(args[2]))
		return args[0] + " " +str(randomlib.randint(min, max))
	else:
		return usage