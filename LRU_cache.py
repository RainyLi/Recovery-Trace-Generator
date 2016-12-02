
import os
import sys

def LRU_cache_trace(parameter_prefix, dir_path, cache_size):
    list = []

    #calculate cache ratio
    request_count=0
    hit_count=0

    cache_space = cache_size
    f_origin_name = parameter_prefix+"_origin.trace"
    f_filtered_name = parameter_prefix+ "_cache=" + str(cache_size) + "_LRU.trace"

    def LRU_kick_out():
        if list:
            list.pop(0)

    if os.path.isfile(dir_path+f_origin_name):
        f_origin = open(dir_path+f_origin_name, 'r')
    else:
        print("from LRU: no such trace exists: " + f_origin_name)
        sys.exit(0)

    f_filtered = open(dir_path+f_filtered_name, 'w')

    # generate trace for disks
    for line in f_origin.readlines():
        request_count = request_count + 1

        line_info = line.split()
        device_number = line_info[1]
        block_number = line_info[2]
        block_position = (device_number, block_number)

        if block_position in list:
            hit_count=hit_count+1
            #print (str(block_position)+"\n")
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

    return (hit_count/request_count, request_count-hit_count)