from FBF_cache import *
from ARC_cache import *
from LFU_cache import *
from LRU_cache import *
from FIFO_cache import *
from NO_cache import *
import os

dir_path = os.path.dirname(os.path.realpath(__file__)) + "\\trace\\"
f_hit_ratio = open(dir_path+"all_hit_raito.csv", 'w')
code_dic={1:"star",2:"triple_star",3:"triple_parity",4:"tip",5:"hdd1"}
f_hit_ratio.write("code,prime,error_disk,stripe_number,cache_size,cache_method,hit_ratio\n")

prime = 5
error_disk = 0
stripe_number = 1
cache_size_range= 20
code=5

# code= 1---star
#       2---triple_star
#       3---triple_parity
#       4---tip
#       5---hdd1
for code in range(1,6):
    parameter_prefix=NO_cache_trace(code, prime, error_disk, stripe_number, dir_path)

    for cache_size in range(1, cache_size_range):
        hit_ratio=FIFO_cache_trace(parameter_prefix, dir_path, cache_size)
        f_hit_ratio.write(code_dic[code] + "," + str(prime) + "," + str(error_disk) + "," + str(stripe_number) + "," + str(
            cache_size) + ",FIFO," + str(hit_ratio) + "\n")

        hit_ratio=LRU_cache_trace(parameter_prefix, dir_path, cache_size)
        f_hit_ratio.write(code_dic[code] + "," + str(prime) + "," + str(error_disk) + "," + str(stripe_number) + "," + str(
            cache_size) + ",LRU," + str(hit_ratio) + "\n")

        hit_ratio =LFU_cache_trace(parameter_prefix, dir_path, cache_size)
        f_hit_ratio.write(code_dic[code] + "," + str(prime) + "," + str(error_disk) + "," + str(stripe_number) + "," + str(
            cache_size) + ",LFU," + str(hit_ratio) + "\n")

        hit_ratio =ARC_cache_trace(parameter_prefix, dir_path, cache_size)
        f_hit_ratio.write(code_dic[code] + "," + str(prime) + "," + str(error_disk) + "," + str(stripe_number) + "," + str(
            cache_size) + ",ARC," + str(hit_ratio) + "\n")

        hit_ratio =FBF_cache_trace(parameter_prefix, dir_path, cache_size)
        f_hit_ratio.write(code_dic[code] + "," + str(prime) + "," + str(error_disk) + "," + str(stripe_number) + "," + str(
            cache_size) + ",FBF," + str(hit_ratio) + "\n")

f_hit_ratio.close()
