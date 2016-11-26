from FBF_cache import *
from ARC_cache import *
from LFU_cache import *
from LRU_cache import *
from FIFO_cache import *
from NO_cache import *
import os

prime = 5
error_disk = 0
stripe_number = 20
cache_size_range= 20
dir_path = os.path.dirname(os.path.realpath(__file__)) + "\\trace\\"

# code= 1---star
#       2---triple_star
#       3---triple_parity
#       4---tip
#       5---hdd1
parameter_prefix=NO_cache_trace(5, prime, error_disk, stripe_number, dir_path)

for cache_size in range(1, cache_size_range):
    FIFO_cache_trace(parameter_prefix, dir_path, cache_size)
    LRU_cache_trace(parameter_prefix, dir_path, cache_size)
    LFU_cache_trace(parameter_prefix, dir_path, cache_size)
    ARC_cache_trace(parameter_prefix, dir_path, cache_size)
    FBF_cache_trace(parameter_prefix, dir_path, cache_size)

# the original recovery request from cpu


