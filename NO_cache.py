from star import *

def origin_trace(recovery_sequence, prime, error_disk, stripe_number, dir_path):
    parameter_prefix="star_p=" + str(prime) + "_error=" + str(error_disk) + "_stripe=" + str(
        stripe_number)
    f_origin_name = parameter_prefix + "_origin.trace"

    f_origin = open(dir_path + f_origin_name, "w")
    error_block_num = len(recovery_sequence)

    for i in range(0, stripe_number):
        for j in range(error_block_num):
            for block_position in recovery_sequence[j]:
                device_number = block_position[0]
                block_number = block_position[1] + error_block_num * i

                origin_trace = '0 ' + str(device_number) + ' ' + str(block_number) + ' 1 1\n'
                f_origin.write(origin_trace)

    f_origin.close()
    return parameter_prefix

def NO_cache_trace(prime, error_disk, stripe_number, dir_path):
    #generate recovery scheme on stripe
    recovery_sequence = star_IO_Generator(prime, error_disk)
    #generate trace on stack given recovery scheme
    return origin_trace(recovery_sequence, prime, error_disk, stripe_number, dir_path)


