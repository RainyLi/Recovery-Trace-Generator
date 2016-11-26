import random

# the stripe scale is (p-1)*(p+2)

def triple_parity_IO_Generator(prime, error_disk):
    recovery_sequence = []
    for i in range(prime - 1):
        # the position of the block to be recovered
        error_block_position = triple_parity_cal((i, error_disk))

        # randomly picking the decoding method: 0==horizontal 1==diagnol 2==anti-diagnol
        recovery_method = random.randint(0, 2)

        # 0---horizontal decoding
        if recovery_method == 0:
            recovery_sequence.append(triple_parity_method0(error_block_position, prime))

        # 1---diagnol decoding
        if recovery_method == 1:
            recovery_sequence.append(triple_parity_method1(error_block_position, prime))

        # 2---anti-diagnol decoding
        if recovery_method == 2:
            recovery_sequence.append(triple_parity_method2(error_block_position, prime))

    return recovery_sequence


def triple_parity_method0(position, p):
    x=position[0]
    y=position[1]
    sequence = []
    for j in range(0, p):
        if j != y:
            block_position = triple_parity_raid((x, j))
            sequence.append(block_position)
    return set(sequence)


def triple_parity_method1(position, p):
    x = position[0]
    y = position[1]
    sequence = []

    i=(x+y)%p

    #blocks on the stripe
    for j in range(p):
        if j!=y and (i-j)%p< p-1:
            block_position=triple_parity_raid(((i-j)%p,j))
            sequence.append(block_position)


    #block on diagnal parity
    if i<p-1:
        block_position = triple_parity_raid((i, p))
        sequence.append(block_position)
    return set(sequence)


def triple_parity_method2(position, p):
    x = position[0]
    y = position[1]
    sequence = []

    i = (x - y) % p

    # blocks on the stripe
    for j in range(p):
        if j != y and (i+j)%p < p-1:
            block_position = triple_parity_raid(((i + j) % p, j))
            sequence.append(block_position)

    # block on diagnal parity
    if i< p-1:
        block_position = triple_parity_raid((i, p+1))
        sequence.append(block_position)
    return set(sequence)


def triple_parity_raid(position):
    #position of cal->raid
    #no diff between raid and cal
    return position


def triple_parity_cal(position):
    # position of raid->cal
    return position