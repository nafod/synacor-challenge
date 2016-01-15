#!/usr/bin/env python3

import os
import sys

prev_newline = False

with open(sys.argv[1], "r") as f:
	for line in f:
		parts = line.split()
		if len(parts) > 1:
			x = 0
			try:
				x = int(parts[1])
			except:
				continue

			if (x >= 32 and x <= 126):
				print(chr(x), end='')
				prev_newline = False
			else:
				if prev_newline == False:
					print("")
					prev_newline = True
