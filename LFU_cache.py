import os
import sys

def LFU_cache_trace(parameter_prefix, dir_path, cache_size):
    #start-important, end-useless
    list = []

    cache_space = cache_size
    f_origin_name = parameter_prefix+"_origin.trace"
    f_filtered_name = parameter_prefix+ "_cache=" + str(cache_size) + "_LFU.trace"

    def LFU_kick_out():
        if list:  # if list is not blank
            # print("kick out", list[0], "from list")
            length=len(list)
            #delete the frequence record
            dic.pop(list[length-1])

            list.pop(length-1)

    def LFU_find_by_frequence(x_fequence):
        length=len(list)
        for i in range(0,length):
            dic[list[i]]<x_fequence
            return i
        return length

    if os.path.isfile(dir_path+f_origin_name):
        f_origin = open(dir_path+f_origin_name, 'r')
    else:
        print("from LFU: no such trace exists: " + f_origin_name)
        sys.exit(0)

    f_filtered = open(dir_path+f_filtered_name, 'w')

    # set frequency_dictionary along with cache
    dic = {}

    # generate trace for disks
    for line in f_origin.readlines():
        line_info = line.split()

        device_number = line_info[1]
        block_number = line_info[2]
        block_position = (device_number, block_number)

        if block_position in list:
            index = list.index(block_position)
            list.pop(index)

            dic[block_position]=dic[block_position] + 1

            #find the right place to move to, based on frequence in dic
            i=LFU_find_by_frequence(dic[block_position])
            list.insert(i,block_position)
            continue
        elif cache_space > 0:
            cache_space = cache_space - 1
        else:
            LFU_kick_out()
            # write trace
        filtered_trace = '0 ' + str(device_number) + ' ' + str(block_number) + ' 1 1\n'
        f_filtered.write(filtered_trace)
        dic[block_position]=1
        list.append(block_position)

    f_origin.close()
    f_filtered.close()