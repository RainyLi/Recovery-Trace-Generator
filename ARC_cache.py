#follow the algorithm of ARC-Journal
# need to check correctness
# in order to fix bug of emptylist.pop(0), added "if" command in some place. Search "emptylist.pop(0)"
import os
import sys

def ARC_cache_trace(parameter_prefix, dir_path, cache_size):
    #start-useless end-important
    T1 = []
    B1 = []
    T2 = []
    B2 = []
    request_count=0
    hit_count=0
    p=0

    # defined outside the loop in order to bde referenced by Replace(p)
    block_position = (0,0)

    c=cache_size

    def Replace(p):
        if len(T1)>=1 and ((block_position in B2 and len(T1)==p) or (len(T1)>p)):
            block=T1[0]
            T1.pop(0)
            B1.append(block)
        else:
            block = T2[0]
            T2.pop(0)
            B2.append(block)

    f_origin_name = parameter_prefix+"_origin.trace"
    f_filtered_name = parameter_prefix+ "_cache=" + str(cache_size) + "_ARC.trace"

    if os.path.isfile(dir_path+f_origin_name):
        f_origin = open(dir_path+f_origin_name, 'r')
    else:
        print("from ARC: no such trace exists: " + f_origin_name)
        sys.exit(0)

    f_filtered = open(dir_path+f_filtered_name, 'w')

    # generate trace for disks
    for line in f_origin.readlines():
        request_count=request_count+1
        line_info = line.split()

        device_number = line_info[1]
        block_number = line_info[2]
        block_position = (device_number, block_number)

        #case1
        if block_position in T1:# cache hit
            hit_count=hit_count+1
            index=T1.index(block_position)
            T1.pop(index)
            T2.append(block_position)
            continue
        elif block_position in T2: #cache hit
            hit_count=hit_count+1
            index = T2.index(block_position)
            T2.pop(index)
            T2.append(block_position)
            continue

        #case2
        elif block_position in B1: #cache miss
            p=min(c, p+max(len(B2)/len(B1),1))
            Replace(p)
            index = B1.index(block_position)
            B1.pop(index)
            T2.append(block_position)
            #disk request
        elif block_position in B2: #cache miss
            p=max(0,p-max(len(B1)/len(B2),1))
            Replace(p)
            index = B2.index(block_position)
            B2.pop(index)
            T2.append(block_position)
            #disk request

        #case3
        else: # cache and ghost both miss
            lenL1 = len(T1) + len(B1)
            lenL2 = len(T2) + len(B2)
            if lenL1==c:
                if len(T1)<c:
                    if B1: # in case of emptylist.pop(0)
                        B1.pop(0)
                    Replace(p)
                else:
                    T1.pop(0)
            elif lenL1<c and lenL1+lenL2>=c:
                if lenL1+lenL2==2*c:
                    if B2: # in case of emptylist.pop(0)
                        B2.pop(0)
                    Replace(p)
            T1.append(block_position)
            #disk request
        filtered_trace = '0 ' + str(device_number) + ' ' + str(block_number) + ' 1 1\n'
        f_filtered.write(filtered_trace)

    f_origin.close()
    f_filtered.close()
    return (hit_count/request_count, request_count-hit_count)