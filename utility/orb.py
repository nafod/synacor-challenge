#!/usr/bin/env python3
import sys
door_value = 30

# We derive this max_steps value from the first solution I manually came up with
# 22 + 4 + 4 + 4 + 4 + 4 - 11 - 1 = 30 (14 steps)
# north -> east -> west -> east -> west -> east -> west -> east -> west -> east ->
# east -> north -> north -> east
max_steps = 14

values = [
		   ["*", 8, "-", 1],
		   [4, "*", 11, "*"],
		   ["+", 4, "-", 18],
		   [22, "-", 9, "*"]
		 ]

stack = [{"x": 3, "y": 0, "trail": [], "orb": 22}]
solutions = []

print("Now processing possible combinations (this may take a while)...")

# Continue while we don't have a solution
while len(stack) > 0:
	current = stack.pop()
	x = current["x"]
	y = current["y"]
	trail = list(current["trail"])
	orb = current["orb"]

	symbol = values[ x ] [ y ]
	trail.append(symbol)

	# Check if we've hit our limit
	if len(trail) == max_steps:
		if x == 0 and y == 3 and orb == 30:
			solutions.append( (len(trail), current) )
		continue

	# If we have a solution, we don't need to build off of it
	if x == 0 and y == 3 and orb == 30:
		solutions.append( (len(trail), current) )
		continue

	if symbol == "+":

		if (x - 1) >= 0:
			node = {"x": x - 1, "y": y, "trail": trail, "orb": orb + values[x-1][y]}
			stack.append(node)

		if (x + 1) < 4:
			# Check that we don't return to the start
			if (x + 1) != 3 and y != 0:
				node = {"x": x + 1, "y": y, "trail": trail, "orb": orb + values[x+1][y]}
				stack.append(node)

		if (y - 1) >= 0:
			node = {"x": x, "y": y - 1, "trail": trail, "orb": orb + values[x][y-1]}
			stack.append(node)

		if (y + 1) < 4:
			node = {"x": x, "y": y + 1, "trail": trail, "orb": orb + values[x][y+1]}
			stack.append(node)

	elif symbol == "-":

		if (x - 1) >= 0:
			node = {"x": x - 1, "y": y, "trail": trail, "orb": orb - values[x-1][y]}
			stack.append(node)

		if (x + 1) < 4:
			node = {"x": x + 1, "y": y, "trail": trail, "orb": orb - values[x+1][y]}
			stack.append(node)

		if (y - 1) >= 0:
			# Check that we don't return to the start
			if x != 3 and (y - 1) != 0:
				node = {"x": x, "y": y - 1, "trail": trail, "orb": orb - values[x][y-1]}
				stack.append(node)

		if (y + 1) < 4:
			node = {"x": x, "y": y + 1, "trail": trail, "orb": orb - values[x][y+1]}
			stack.append(node)

	elif symbol == "*":

		if (x - 1) >= 0:
			node = {"x": x - 1, "y": y, "trail": trail, "orb": orb * values[x-1][y]}
			stack.append(node)

		if (x + 1) < 4:
			node = {"x": x + 1, "y": y, "trail": trail, "orb": orb * values[x+1][y]}
			stack.append(node)

		if (y - 1) >= 0:
			node = {"x": x, "y": y - 1, "trail": trail, "orb": orb * values[x][y-1]}
			stack.append(node)

		if (y + 1) < 4:
			node = {"x": x, "y": y + 1, "trail": trail, "orb": orb * values[x][y+1]}
			stack.append(node)

	else:

		if (x - 1) >= 0:
			node = {"x": x - 1, "y": y, "trail": trail, "orb": orb}
			stack.append(node)

		if (x + 1) < 4:
			node = {"x": x + 1, "y": y, "trail": trail, "orb": orb}
			stack.append(node)

		if (y - 1) >= 0:
			node = {"x": x, "y": y - 1, "trail": trail, "orb": orb}
			stack.append(node)

		if (y + 1) < 4:
			node = {"x": x, "y": y + 1, "trail": trail, "orb": orb}
			stack.append(node)

print("Completed!")

print("Solutions:")

solutions = sorted(solutions)
for s in solutions:
	print(s)
