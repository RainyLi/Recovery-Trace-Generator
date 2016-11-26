#diagonal and anti-diagonal parity blocks are integrated into data disks
#hence must be dealt with once founded in the error disk


############还没有检测正确性---?真的是错的。。。。----update: ensure correctness when error disk is 0
import random

# the stripe scale is (p-1)*(p+1)

def tip_IO_Generator(prime, error_disk):
    recovery_sequence = []
    for i in range(prime - 1):
        # the position of the block to be recovered
        error_block_position = tip_cal((i, error_disk))

        #if error_block is diagonal parity block
        if i+1==error_disk:
            recovery_method=1
        #elif error_block is anti-diagonal parity block
        elif prime-1-i==error_disk:
            recovery_method=2
        # randomly picking the decoding method: 0==horizontal 1==diagnol 2==anti-diagnol
        else:
            recovery_method = random.randint(0, 2)
            #recovery_method=2

        # 0---horizontal decoding
        if recovery_method == 0:
            recovery_sequence.append(tip_method0(error_block_position, prime))

        # 1---diagnol decoding
        if recovery_method == 1:
            recovery_sequence.append(tip_method1(error_block_position, prime))

        # 2---anti-diagnol decoding
        if recovery_method == 2:
            recovery_sequence.append(tip_method2(error_block_position, prime))

    return recovery_sequence


def tip_method0(position, p):
    x=position[0]
    y=position[1]
    sequence = []

    i=x
    for j in range(0, p + 1):
        if j != y and i+1!=j and i+j!=p-1:
            block_position = tip_raid((i, j))
            sequence.append(block_position)
    return set(sequence)


def tip_method1(position, p):
    x = position[0]
    y = position[1]
    sequence = []

    if y==x+1: #if the error block is parity block
        i=x
    else:      #else the error block is data block
        i=(x+y)%p

    # data blocks on the strip
    for j in range(p):
        if j!=y and (i-j)%p!=p-1 and (i-j)%p+1!=j:
            block_position=tip_raid(((i-j)%p, j))
            sequence.append(block_position)

    # parity block on the strip
    if not (i==x and y==i+1):
        block_position = tip_raid((i, i+1))
        sequence.append(block_position)
    return set(sequence)


def tip_method2(position, p):
    x = position[0]
    y = position[1]
    sequence = []

    if y==p-1-x:    # if error block is parity block
        i=x
    else:           # if error block is data block
        i=(x-y)%p

    # data blocks on the strip
    for j in range(p):
        if j!=y and (i+j)%p!=p-1 and (i+j)%p+j!=p-1:
            block_position=tip_raid(((i+j)%p, j))
            sequence.append(block_position)

    # parity blocks on the strip
    if not (i==x and y==p-1-i):
        block_position = tip_raid((i, p-1-i))
        sequence.append(block_position)
    return set(sequence)

def tip_raid(position):
    # position of cal->raid
    return position

def tip_cal(position):
    # position of raid->cal
    return position