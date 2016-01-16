import itertools

nums = [2, 3, 5, 7, 9]

a = 0
b = 0
c = 0
d = 0
e = 0

sums = []

for x in itertools.permutations(nums):
	# _ + _ * _^2 + _^3 - _ = 399
	val = x[0] + x[1] * (x[2]**2) + (x[3]**3) - x[4]
	sums.append(val)
	if val == 399:
		print x

print sorted(sums)
