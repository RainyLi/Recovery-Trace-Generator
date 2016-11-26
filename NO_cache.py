from star import *
from triple_star import *
from triple_parity import *
from tip import *
from hdd1 import *

def origin_trace(recovery_sequence, code, prime, error_disk, stripe_number, dir_path):
    if code==1:
        parameter_prefix = "star"
    elif code==2:
        parameter_prefix = "triple_star"
    elif code==3:
        parameter_prefix = "triple_parity"
    elif code==4:
        parameter_prefix = "tip"
    elif code==5:
        parameter_prefix = "hdd1"
    parameter_prefix=parameter_prefix+"_p=" + str(prime) + "_error=" + str(error_disk) + "_stripe=" + str(
        stripe_number)
    f_origin_name = parameter_prefix + "_origin.trace"

    f_origin = open(dir_path + f_origin_name, "w")
    error_block_num = len(recovery_sequence)

    for i in range(0, stripe_number):
        for j in range(error_block_num):
            for block_position in recovery_sequence[j]:
                device_number = block_position[1]
                block_number = block_position[0] + error_block_num * i

                origin_trace = '0 ' + str(device_number) + ' ' + str(block_number) + ' 1 1\n'
                f_origin.write(origin_trace)

    f_origin.close()
    return parameter_prefix

def NO_cache_trace(code, prime, error_disk, stripe_number, dir_path):
    #generate recovery scheme on stripe
    if code==1:
        recovery_sequence = star_IO_Generator(prime, error_disk)
    elif code==2:
        recovery_sequence = triple_star_IO_Generator(prime, error_disk)
    elif code==3:
        recovery_sequence = triple_parity_IO_Generator(prime, error_disk)
    elif code==4:
        recovery_sequence = tip_IO_Generator(prime, error_disk)
    elif code==5:
        recovery_sequence = hdd1_IO_Generator(prime, error_disk)
    #generate trace on stack given recovery scheme
    return origin_trace(recovery_sequence, code, prime, error_disk, stripe_number, dir_path)


