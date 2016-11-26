import random

# the stripe scale is (p-1)*(p+2)

def triple_star_IO_Generator(prime, error_disk):
    recovery_sequence = []
    #for each block in the error disk
    for i in range(0, prime-1):
        # the position of the block(i, error_disk) to be recovered
        # the position is for calculation
        error_block_position = triple_star_cal((i, error_disk))

        # randomly picking the decoding method: 0==horizontal 1==anti_diagnol 2==diagnol
        recovery_method = random.randint(0, 2)

        # 0---horizontal decoding
        if recovery_method == 0:
            recovery_sequence.append(triple_star_method0(error_block_position, prime))

        # 1---anti_diagnol decoding
        if recovery_method == 1:
            recovery_sequence.append(triple_star_method1(error_block_position, prime))

        # 2---diagnol decoding
        if recovery_method == 2:
            recovery_sequence.append(triple_star_method2(error_block_position, prime))

    return recovery_sequence


def triple_star_method0(position, p):
    x=position[0]
    y=position[1]
    sequence = []
    for j in range(0, p):
        if j != y:
            block_position = triple_star_raid((x, j))
            sequence.append(block_position)
    return set(sequence)


def triple_star_method1(position, p):
    x = position[0]
    y = position[1]
    sequence = []

    # the parity's i
    i=(x-y)%p

    # the position of the strip
    for j in range(p):
        if j!=y and (i+j)%p != 0:
            block_position=triple_star_raid(((i+j)%p, j))
            sequence.append(block_position)

    # the position of the parity
    if i!=0:
        block_position=triple_star_raid((i, p))
        sequence.append(block_position)

    return set(sequence)


def triple_star_method2(position, p):
    x = position[0]
    y = position[1]
    sequence = []

    # the parity's i
    i = (x + y) % p

    # the position of the strip
    for j in range(p):
        if j != y and (i - j) % p != 0:
            block_position = triple_star_raid(((i - j) % p, j))
            sequence.append(block_position)

    # the position of the parity
    if i!=0:
        block_position = triple_star_raid((i, p+1))
        sequence.append(block_position)

    return set(sequence)


def triple_star_raid(position):
    # position in cal->position in raid
    x=position[0]
    y=position[1]
    return(x-1,y)

def triple_star_cal(position):
    # position in raid->position in calculation
    x = position[0]
    y = position[1]
    return (x+1, y)