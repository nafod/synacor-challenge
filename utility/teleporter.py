#!/usr/bin/env python3
import sys
x = 4
y = 1
z = 1
stack = []

# This version is essentially line-for-line what the
# unoptimized assembly version from the binary does
def original():
	global x, y, z, stack
	if x > 0:

		if y > 0:
			stack.append(x)
			y = y - 1
			a()
			y = x
			x = stack.pop() - 1
		else:
			x = x - 1
			y = z

		a()

	else:
		x = y + 1

def optimized():
	global x, y, z, stack
	stack = [0, 0, 0, 0, 0] # positions 0-4
	while stack != [0, 0, 0, 0, 0] or x > 0:

		# Special case for x = 3
		if stack[0:3] == [0, 0, 0] and stack[4] == 0 and x == 2:
			base = y
			prev = base
			power = (z + 1) ** 3
			while stack[3] > 0:
				base = (base + power) % 32768

				power = (power * (z+1)) % 32768
				stack[3] = stack[3] - 1
			stack[2] = base
			x = 0
			y = z * 2

		while x > 0:
			stack[x] = stack[x] + y
			x = x - 1
			y = z

		# Process the stack elements
		while True:
			x = x + 1

			if x == len(stack):
				x = 1
				stack = [0, 0, 0, 0, 0]
				break

			if (stack[x] == 0):
				continue

			if x == 2:
				y = ( y + (z + 1) * stack[x] ) % 32768
				stack[x] = 0
				continue

			if (x - 1) > 0:
				y = y + 1
				stack[x] = stack[x] - 1
				break

			y = ( y + stack[x] ) % 32768
			stack[x] = 0

		x = x - 1

	y = y % 32768
	x = (y + 1) % 32768

z = 1
while z < 32768:
	x = 4
	y = 1
	optimized()
	print (x, y, z)
	sys.stdout.flush()
	if x == 6:
		print("\t--> found!")
		break

	z = z + 1

if z == 32768:
	print("no solution found!")
