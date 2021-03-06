# star, triple star, triple parity only consider the single disk recovery of the data disk
# while in hdd1, there is no separation of data disk and parity disk in horizontal and anti-diagnol stripe,
# hence data block and parity block should be recovered together

import random

# the stripe scale is (p-1)*(p+1)

def hdd1_IO_Generator(prime, error_disk):
    recovery_sequence = []
    for i in range(prime - 1):
        # the position of the block to be recovered
        error_block_position = hdd1_cal((i, error_disk))

        # randomly picking the decoding method: 0==horizontal 1==anti-diagnol 2==diagnol

        if i==prime-2 and (error_disk - i)% prime==(prime-1): # only anti-diagnol parity is yes
            recovery_method=1
        elif i==prime-2: # if error block is anti-diagnol parity
            recovery_method= random.choice([1,2])
        elif (error_disk - i)% prime==(prime-1): # if error block is missed by diagnol parity
            recovery_method = random.choice([0,1])
        else:
            #recovery_method = random.randint(0, 2)
            recovery_method=2

        # 0---horizontal decoding
        if recovery_method == 0:
            recovery_sequence.append(hdd1_method0(error_block_position, prime))

        # 1---anti-diagnol decoding
        if recovery_method == 1:
            recovery_sequence.append(hdd1_method1(error_block_position, prime))

        # 2---diagnol decoding
        if recovery_method == 2:
            recovery_sequence.append(hdd1_method2(error_block_position, prime))

    return recovery_sequence


def hdd1_method0(position, p):
    x=position[0]
    y=position[1]
    sequence = []
    for j in range(0, p):
        if j != y:
            block_position = hdd1_raid((x, j))
            sequence.append(block_position)
    return set(sequence)


def hdd1_method1(position, p):
    x = position[0]
    y = position[1]
    sequence = []

    # the data block on strip
    j=(y+x+2)%p

    for i in range(p-2) :
        if (p-3-i)%p !=x:
            block_position=hdd1_raid(((p-3-i)%p, (i+j+1)%p))
            sequence.append(block_position)

    # the parity block on strip
    if x!=p-2:
        block_position = hdd1_raid((p-2, j))
        sequence.append(block_position)
    return set(sequence)


def hdd1_method2(position, p):
    x = position[0]
    y = position[1]
    sequence = []

    if x==2:
        x=x

    # the data block on the strip
    j=(y-x)%p
    for i in range(p-1):
        if i!=x:
            block_position=hdd1_raid((i, (i+j)%p))
            sequence.append(block_position)

    # the parity block on the strip
    block_position = hdd1_raid((j, p))
    sequence.append(block_position)
    return set(sequence)

def hdd1_raid(position):
    return position

def hdd1_cal(position):
    return position