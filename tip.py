#diagonal and anti-diagonal parity blocks are integrated into data disks
#hence must be dealt with once founded in the error disk


############还没有检测正确性
import random

# the stripe scale is (p-1)*(p+1)

def tip_IO_Generator(prime, error_disk):
    recovery_sequence = []
    for i in range(prime - 1):
        # the position of the block to be recovered
        error_block_position = tip_position(i, error_disk, prime)

        #if error_block is diagonal parity block
        if i+1==error_disk:
            recovery_method=1
        #elif error_block is anti-diagonal parity block
        elif prime-1-i==error_disk:
            recovery_method=2
        # randomly picking the decoding method: 0==horizontal 1==diagnol 2==anti-diagnol
        else:
            recovery_method = random.randint(0, 2)
            #recovery_method=1

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
    (x, y) = tip_xy_decoder(position, p)
    sequence = []

    i=x
    for j in range(0, p + 1):
        if j != y and i+1!=j and i+j!=p-1:
            block_position = tip_position(i, j, p)
            sequence.append(block_position)
    return set(sequence)


def tip_method1(position, p):
    (x, y) = tip_xy_decoder(position, p)
    sequence = []

    if y==x+1: #if the error block is parity block
        i=x
    else:      #else the error block is data block
        i=(x+y)%p

    # data blocks on the strip
    for j in range(p):
        if j!=y and (i-j)%p!=p-1 and (i-j)%p+1!=j:
            block_position=tip_position((i-j)%p, j, p)
            sequence.append(block_position)

    # parity block on the strip
    if i!=x:
        block_position = tip_position(i, i+1, p)
        sequence.append(block_position)
    return set(sequence)


def tip_method2(position, p):
    (x, y) = tip_xy_decoder(position, p)
    sequence = []

    if y==p-1-x:    # if error block is parity block
        i=x
    else:           # if error block is data block
        i=(x-y)%p

    # data blocks on the strip
    for j in range(p):
        if j!=y and (i+j)%p!=p-1 and (i+j)%p+j!=p-1:
            block_position=tip_position((i+j)%p, j, p)
            sequence.append(block_position)

    # parity blocks on the strip
    if i!=x:
        block_position = tip_position(i, p-1-i, p)
        sequence.append(block_position)
    return set(sequence)

def tip_position(x, y, p):
    return x * (p + 1) + y

def tip_xy_decoder(position, p):
    x = int(position / (p + 1))
    y = position % (p + 1)
    return (x, y)