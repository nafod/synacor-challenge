#!/usr/bin/env python3
import sys
import readline

data = ([0] * 32768)
eip = 0
registers = [0, 0, 0, 0, 0, 0, 0, 0]
REGISTER_MAGIC_SHIFT = 32768
MAX_LITERAL = 32767
MAX_REGISTER = 32775
stack = []
input_buffer = ""
breakpoints = []
watches = []
debug_flags = {"flag_mem_writes": False, "flag_mem_reads": False}

def decompile_instruction(d, count):
	instructions = ["halt", "set", "push", "pop", "eq", "gt", "jmp", "jt", "jf", "add", "mult", "mod", "and", "or", "not", "rmem", "wmem", "call", "ret", "out", "in", "noop"]
	num_arguments = [0, 2, 1, 1, 3, 3, 1, 2, 2, 3, 3, 3, 3, 3, 2, 2, 2, 1, 0, 1, 1, 0]

	instruction = instructions[d[count]]
	args = ""
	for x in range(num_arguments[d[count]]):
		temp = d[count + 1 + x]
		if d[count + 1 + x] <= MAX_LITERAL:
			temp = str(d[count + 1 + x])
		else:
			temp = "reg" + str((d[count + 1 + x] - REGISTER_MAGIC_SHIFT))
		args = args + temp + " "

	buffer = "%d: %4s %s" % (count, instruction, args)

	return buffer

def processDebug(loc):
	global input_buffer
	while True:
		command = input("Debug input: ")
		parts = command.split()

		if len(parts) == 0:
			continue

		if parts[0] == "print":

			val = 0
			num = int(parts[1])

			if num <= MAX_LITERAL:
				val = data[num]
			elif num > MAX_LITERAL and num <= MAX_REGISTER:
				val = registers[num - REGISTER_MAGIC_SHIFT]

			print("value: %d" % val)
		elif parts[0] == "set":
			set_num_value(int(parts[1]), int(parts[2]))
			print("value updated")
		elif parts[0] == "break":
			breakpoints.append(int(parts[1]))
			print("breakpoint updated")
		elif parts[0] == "continue":
			print("continuing")
			break
		elif parts[0] == "step":
			return "step"
		elif parts[0] == "jump":
			stack.append(loc)
			return int(parts[1])
		elif parts[0] == "reset":
			sys.exit(0)
		elif parts[0] == "dump":
			decompile(data)
		elif parts[0] == "input":
			input_buffer = input_buffer + command[6:] + "\n"
			print("updated input: [%s]" % input_buffer)
		elif parts[0] == "flag":
			debug_flags[parts[1]] = (True if parts[2] == "true" else False)
		elif parts[0] == "watch":
			watches.append(int(parts[1]))
		else:
			print("invalid command")

	return -1

def decompile(d):
	count = 0
	instructions = ["halt", "set", "push", "pop", "eq", "gt", "jmp", "jt", "jf", "add", "mult", "mod", "and", "or", "not", "rmem", "wmem", "call", "ret", "out", "in", "noop"]
	num_arguments = [0, 2, 1, 1, 3, 3, 1, 2, 2, 3, 3, 3, 3, 3, 2, 2, 2, 1, 0, 1, 1, 0]

	while count < len(d):
		try:
			instruction = instructions[d[count]]
		except:
			# Must be just data
			print("%5d: %4s" % (count, d[count]))
			count = count + 1
			continue
		args = ""
		for x in range(num_arguments[d[count]]):
			temp = d[count + 1 + x]
			if d[count + 1 + x] <= MAX_LITERAL:
				temp = str(d[count + 1 + x])
			else:
				temp = "reg" + str((d[count + 1 + x] - REGISTER_MAGIC_SHIFT))
			args = args + temp + " "

		# Format output
		if instruction == "out":
			# Special case for ascii characters
			buffer = "\"" + chr(d[count+1])
			x = 2
			while(True):
				if instructions[d[count+x]] == "out":
					buffer = buffer + chr(d[count+x+1])
					x = x + 2
				else:
					break

			print("%5d: %4s %s" % (count, instruction, buffer + "\""))
			count = count + x - 2
		else:
			print("%5d: %4s %s" % (count, instruction, args))
		count = count + 1 + num_arguments[d[count]]

def get_num_value(num):
	if num <= MAX_LITERAL:
		return num
	elif num > MAX_LITERAL and num <= MAX_REGISTER:
		return registers[num - REGISTER_MAGIC_SHIFT]
	else:
		print("Invalid number (%s)" % (num))
		return "INVALID"

def set_num_value(where, value):
	if where <= MAX_LITERAL:
		data[where] = value
	elif where > MAX_LITERAL and where <= MAX_REGISTER:
		registers[where - REGISTER_MAGIC_SHIFT] = value
	else:
		print("Invalid destination (%s)" % (num))

try:
	temp = 0
	with open(sys.argv[1], 'rb') as f:
		vals = f.read(2)
		while len(vals) > 0:
			data[temp] = (int(vals[1]) << 8) + int(vals[0])
			vals = f.read(2)
			temp = temp + 1
except:
	print("Please specify binary file")
	sys.exit(1)

#decompile(data)
#print(1/0)

halted = False
debugging = False
step = False

while not halted:

	if (debugging and step is True) or eip in breakpoints:
		print("-----------------------------")
		print(decompile_instruction(data, eip))
		#print ("%s %s %s %s" % (data[eip], data[eip + 1], data[eip + 2], data[eip + 3]))
		print ("registers: %s" % registers)
		print ("stack: %s" % stack)
		step = False
		ret = processDebug(eip)
		if ret == "step":
			step = True
		elif ret > 0:
			eip = ret

	# Process instructions from data based on EIP
	instruction = data[eip]
	if instruction == 0:
		# halt
		halted = True
	elif instruction == 1:
		# set register <a> to the value of <b>
		a = data[eip + 1]
		b = data[eip + 2]
		registers[a - REGISTER_MAGIC_SHIFT] = get_num_value(b)
		eip = eip + 3
	elif instruction == 2:
		# push <a> onto the stack
		a = data[eip + 1]
		stack.append(get_num_value(a))
		eip = eip + 2
	elif instruction == 3:
		# remove the top element from the stack and write it into <a>; empty stack = error
		a = data[eip + 1]
		if len(stack) > 0:
			set_num_value(a, stack.pop())
		else:
			print("Error popping value from stack")
		eip = eip + 2
	elif instruction == 4:
		# set <a> to 1 if <b> is equal to <c>; set it to 0 otherwise
		a = data[eip + 1]
		b = data[eip + 2]
		c = data[eip + 3]
		if get_num_value(b) == get_num_value(c):
			set_num_value(a, 1)
		else:
			set_num_value(a, 0)
		eip = eip + 4
	elif instruction == 5:
		# set <a> to 1 if <b> is greater than <c>; set it to 0 otherwise
		a = data[eip + 1]
		b = data[eip + 2]
		c = data[eip + 3]
		if get_num_value(b) > get_num_value(c):
			set_num_value(a, 1)
		else:
			set_num_value(a, 0)
		eip = eip + 4
	elif instruction == 6:
		# jump to <a>
		a = data[eip + 1]
		eip = get_num_value(a)
	elif instruction == 7:
		# if <a> is nonzero, jump to <b>
		a = data[eip + 1]
		b = data[eip + 2]
		if get_num_value(a) > 0:
			eip = get_num_value(b)
		else:
			eip = eip + 3
	elif instruction == 8:
		# if <a> is zero, jump to <b>
		a = data[eip + 1]
		b = data[eip + 2]
		if get_num_value(a) == 0:
			eip = get_num_value(b)
		else:
			eip = eip + 3
	elif instruction == 9:
		# assign into <a> the sum of <b> and <c> (modulo 32768)
		a = data[eip + 1]
		b = data[eip + 2]
		c = data[eip + 3]
		set_num_value(a, (get_num_value(b) + get_num_value(c)) % 32768)
		eip = eip + 4
	elif instruction == 10:
		# store into <a> the product of <b> and <c> (modulo 32768)
		a = data[eip + 1]
		b = data[eip + 2]
		c = data[eip + 3]
		set_num_value(a, (get_num_value(b) * get_num_value(c)) % 32768)
		eip = eip + 4
	elif instruction == 11:
		# store into <a> the remainder of <b> divided by <c>
		a = data[eip + 1]
		b = data[eip + 2]
		c = data[eip + 3]
		set_num_value(a, (get_num_value(b) % get_num_value(c)) % 32768)
		eip = eip + 4
	elif instruction == 12:
		# stores into <a> the bitwise and of <b> and <c>
		a = data[eip + 1]
		b = data[eip + 2]
		c = data[eip + 3]
		set_num_value(a, (get_num_value(b) & get_num_value(c)) % 32768)
		eip = eip + 4
	elif instruction == 13:
		# stores into <a> the bitwise or of <b> and <c>
		a = data[eip + 1]
		b = data[eip + 2]
		c = data[eip + 3]
		set_num_value(a, (get_num_value(b) | get_num_value(c)) % 32768)
		eip = eip + 4
	elif instruction == 14:
		# stores 15-bit bitwise inverse of <b> in <a>
		a = data[eip + 1]
		b = data[eip + 2]
		set_num_value(a, (~get_num_value(b)) % 32768)
		eip = eip + 3
	elif instruction == 15:
		# read memory at address <b> and write it to <a>
		a = data[eip + 1]
		b = data[eip + 2]
		set_num_value(a, data[get_num_value(b)])
		if debug_flags["flag_mem_reads"]:
			print("READ: read %s into %s" % (data[get_num_value(b)], get_num_value(a)))
		elif get_num_value(a) in watches:
			print("WATCH: read %s into %s" % (data[get_num_value(b)], get_num_value(a)))
		eip = eip + 3
	elif instruction == 16:
		# write the value from <b> into memory at address <a>
		a = data[eip + 1]
		b = data[eip + 2]
		data[get_num_value(a)] = get_num_value(b)
		if debug_flags["flag_mem_writes"]:
			print("WRITE: wrote %s into %s" % (get_num_value(b), get_num_value(a)))
		elif get_num_value(a) in watches:
			print("WATCH: wrote %s into %s" % (get_num_value(b), get_num_value(a)))
		eip = eip + 3
	elif instruction == 17:
		# write the address of the next instruction to the stack and jump to <a>
		a = data[eip + 1]
		stack.append(eip + 2)
		eip = get_num_value(a)
	elif instruction == 18:
		if len(stack) > 0:
			eip = stack.pop()
		else:
			print("No RET address on stack")
	elif instruction == 19:
		# write the character represented by ascii code <a> to the terminal
		a = data[eip + 1]
		print(chr(get_num_value(a)), end='')
		eip = eip + 2
	elif instruction == 20:
		# read a character from the terminal and write its ascii code to <a>;
		# it can be assumed that once input starts, it will continue until a newline is encountered;
		# this means that you can safely read whole lines from the keyboard and trust that they will be fully read
		a = data[eip + 1]
		if len(input_buffer) == 0:
			input_buffer = input() + "\n"

			# Special
			if input_buffer == "debug\n":
				step = True
				debugging = True
				input_buffer = ""
				continue

		set_num_value(a, ord(input_buffer[0]))
		input_buffer = input_buffer[1:]
		eip = eip + 2
	elif instruction == 21:
		# no operation
		eip = eip + 1
	else:
		print("Invalid instruction: %s" % instruction)
