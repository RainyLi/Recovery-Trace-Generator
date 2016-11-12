#same problem as FBF

import os
import sys

def LRU_cache_trace(parameter_prefix, dir_path, cache_size):
    list = []

    cache_space = cache_size
    f_origin_name = parameter_prefix+"_origin.trace"
    f_filtered_name = parameter_prefix+ "_cache=" + str(cache_size) + "_LRU.trace"

    def LRU_kick_out():
        if list:  # if list is not blank
            # print("kick out", list[0], "from list")
            list.pop(0)

    if os.path.isfile(dir_path+f_origin_name):
        f_origin = open(dir_path+f_origin_name, 'r')
    else:
        print("from FBF: no such trace exists: " + f_origin_name)
        sys.exit(0)

    f_filtered = open(dir_path+f_filtered_name, 'w')

    # generate trace for disks
    for line in f_origin.readlines():
        line_info = line.split()

        device_number = line_info[1]
        block_number = line_info[2]
        block_position = (device_number, block_number)

        if block_position in list:
            index = list.index(block_position)
            list.pop(index)
            list.append(block_position)
            continue
        elif cache_space > 0:
            cache_space = cache_space - 1
        else:
            LRU_kick_out()
            # write trace
        filtered_trace = '0 ' + str(device_number) + ' ' + str(block_number) + ' 1 1\n'
        f_filtered.write(filtered_trace)
        list.append(block_position)

    f_origin.close()
    f_filtered.close()