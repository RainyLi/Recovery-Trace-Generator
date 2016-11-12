import random

# the stripe scale is (p-1)*(p+3)
# position is defined as (x,y) instead of a number
# bug: error disk is only allowed to be disk0, code remains to be improved to allow other disk(see comments in method2)

def star_IO_Generator(prime, error_disk):
	recovery_sequence=[]
	for i in range(prime-1):
		#the position of the block to be recovered
		error_block_position=(i,error_disk)
	
		#randomly picking the decoding method: 0==horizontal 1==diagnol 2==anti-diagnol
		#recovery_method=random.randint(0,2)
		recovery_method=2

		#0---horizontal decoding
		if recovery_method==0:
			recovery_sequence.append(star_method0(error_block_position,prime))
	
		#1---diagnol decoding
		if recovery_method==1:
			recovery_sequence.append(star_method1(error_block_position,prime))
		
		# 2---anti-diagnol decoding
		if recovery_method==2:
			recovery_sequence.append(star_method2(error_block_position, prime))

	return recovery_sequence

def star_method0(position, p):
	(x, y) = position
	sequence = []
	for j in range(0, p + 1):
		if j != y:
			block_position = (x, j)
			sequence.append(block_position)
	return set(sequence)

def star_method1(position, p):
	(x, y) = position
	sequence = []

	# if error block is on S1
	if x == (p - 1 - y) % p:
		# read the two parity columns first
		for i in range(0, p - 1):
			block_position = (i, p + 1)
			sequence.append(block_position)
			block_position = (i, p)
			sequence.append(block_position)

		# read S1 blocks except the error block
		for j in range(1, p):
			if j != y:
				block_position = ((p - 1 - j) % p, j)
				sequence.append(block_position)
		return set(sequence)

	# blocks on S1
	for j in range(1, p):
		block_position = ((p - 1 - j) % p, j)
		sequence.append(block_position)

	# block on the strip
	i = (x + y) % p

	for j in range(0, p):
		if (j != y) & ((i - j) % p != (p - 1)):
			block_position = ((i - j) % p, j)
			sequence.append(block_position)

	block_position = (i, p + 1)
	sequence.append(block_position)
	return set(sequence)

def star_method2(position, p):
	(x, y) = position
	sequence = []

	# if error block is on S2
	if x == (y - 1) % p:
		# read the two parity columns first
		for i in range(0, p - 1):
			block_position = (i, p + 2)
			sequence.append(block_position)
			block_position = (i, p)
			sequence.append(block_position)

		# read S2 blocks except the error block
		for j in range(1, p):
			if j != y:
				block_position = ((j - 1) % p, j)
				sequence.append(block_position)
		return set(sequence)

	# blocks on S2
	# there is a bug here--what if s2 blocks has error? Only disk0 is allowed to occure error
	for j in range(1, p):
		block_position = ((j - 1) % p, j)
		sequence.append(block_position)

	# blocks on strip
	i = (x - y) % p

	for j in range(0, p):
		if (j != y) & ((i + j) % p != (p - 1)):
			block_position = ((i + j) % p, j)
			sequence.append(block_position)

	block_position = (i, p + 2)
	sequence.append(block_position)
	return set(sequence)