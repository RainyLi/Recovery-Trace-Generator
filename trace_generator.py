from FBF_cache import *
from LRU_cache import *
from NO_cache import *
import os

prime = 5
error_disk = 0
stripe_number = 20
cache_size= 20
dir_path = os.path.dirname(os.path.realpath(__file__)) + "\\trace\\"

parameter_prefix=NO_cache_trace(prime, error_disk, stripe_number, dir_path)
LRU_cache_trace(parameter_prefix, dir_path, cache_size)
FBF_cache_trace(parameter_prefix, dir_path, cache_size)

# the original recovery request from cpu


