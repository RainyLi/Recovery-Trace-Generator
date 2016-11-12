#need to add check file whether exists part
#need to check the correctness
#file shoud not be limited by prime, error_disk(heritage name from original file)
#did not consider when dictionary_priority==0, might not necessary but better to be complete
import os
import sys

def FBF_kick_out(list3,list2, list1):
    if list1: # if list1 is not blank
        #print("kick out", list1[0], "from list1")
        list1.pop(0)
    elif list2:
        #print("kick out", list2[0], "from list2")
        list2.pop(0)
    elif list3:
        #print("kick out", list3[0], "from list3")
        list3.pop(0)
    else:
        return -1 #failed, nothing to be kicked out
    return (list3, list2, list1) #succeed

def FBF_cache_trace(parameter_prefix, dir_path, cache_size):
    list3 = []
    list2 = []
    list1 = []

    cache_space = cache_size
    f_origin_name = parameter_prefix+ "_origin.trace"
    f_FBF_name = parameter_prefix + "_cache=" + str(cache_size) + "_FBF.trace"

    if os.path.isfile(dir_path+f_origin_name):
        f_origin = open(dir_path+f_origin_name, 'r')
    else:
        print("from FBF: no such trace exists: " + f_origin_name)
        sys.exit(0)

    f_FBF = open(dir_path+f_FBF_name, 'w')

    # set priority_dictionary according to origin trace
    # should be calculate in cpu and set to cache together with io requests
    dic = {}
    for line in f_origin.readlines():
        line_info = line.split()

        device_number = line_info[1]
        block_number = line_info[2]
        block_position = (device_number, block_number)

        if block_position in dic:
            dic[block_position] = dic[block_position] + 1
        else:
            dic[block_position] = 1

    # generate trace for disks
    f_origin.seek(0, 0)  # set pointer to start
    for line in f_origin.readlines():
        line_info = line.split()

        device_number = line_info[1]
        block_number = line_info[2]
        block_position = (device_number, block_number)

        block_priority = dic[block_position]
        dic[block_position] = dic[block_position] - 1

        if block_priority == 3:  # must not be in cache
            if cache_space > 0:
                # print("fetch a free block")
                cache_space = cache_space - 1
            else:
                FBF_kick_out(list3, list2, list1)

            list3.append(block_position)
            # write trace
            FBF_trace = '0 ' + str(device_number) + ' ' + str(block_number) + ' 1 1\n'
            f_FBF.write(FBF_trace)
            continue

        if block_priority == 2:
            if block_position in list3:
                index = list3.index(block_position)
                list3.pop(index)
                list2.append(block_position)
                # print("degrade", j, "from List3 to List2")
                continue
            if cache_space > 0:
                # print("fetch a free block")
                cache_space = cache_space - 1
            else:
                FBF_kick_out(list3, list2, list1)

            # write trace
            FBF_trace = '0 ' + str(device_number) + ' ' + str(block_number) + ' 1 1\n'
            f_FBF.write(FBF_trace)
            # print("append", block_position, " to List2")
            list2.append(block_position)

            continue

        if block_priority == 1:
            if block_position in list2:
                index = list2.index(block_position)
                list2.pop(index)
                list1.append(block_position)
                # print("degrade", j, "from List2 to List1")
                continue
            if cache_space > 0:
                # print("fetch a free block")
                cache_space = cache_space - 1
            else:
                FBF_kick_out(list3, list2, list1)

            # write to filter
            FBF_trace = '0 ' + str(device_number) + ' ' + str(block_number) + ' 1 1\n'
            f_FBF.write(FBF_trace)
            # print("append", j, " to List1")
            list1.append(block_position)
            continue

    f_origin.close()
    f_FBF.close()