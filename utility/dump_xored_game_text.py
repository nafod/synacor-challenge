#!/usr/bin/env python3

import os
import sys

prev_line = ""
data = {}
offsets = {}

with open(sys.argv[1], "r") as f:
	lines = f.readlines()
	for x in range(0, len(lines)):
		line = lines[x]

		try:
			vals = line.split(":")
			data[int(vals[0])] = vals[1]
		except:
			prev_line = line
			continue

		if "set reg1 1531" in line:

			# Let's pull out the key for each XOR'd string offset
			offset_loc = int(prev_line.split()[-1])
			key_parts = lines[x+1].split()
			key = int(key_parts[-1]) + int(key_parts[-2])

			offsets[offset_loc] = key

		prev_line = line

for temp in offsets:
	try:
		length = int(data[temp])
		x = 1
		print("%s: " % temp, end='')
		while x < length:
			val = int(data[temp + x]) ^ offsets[temp]
			print(chr(val), end='')
			x = x + 1
		print("")
	except:
		continue
