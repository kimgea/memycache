'''
Created on 8. juni 2014

@author: Kim-Georg Aase


NOTE: it is better to just store the two last numbers in the fibonacci method
'''

import memycache

     

def fibonacci( n ):
    if n in ( 0, 1 ):
        return n
    return fibonacci( n - 1 ) + fibonacci( n - 2 )
    
@memycache.Eternal   
def eternal_cached_fib( n ):
    if n in ( 0, 1 ):
        return n
    return eternal_cached_fib( n - 1 ) + eternal_cached_fib( n - 2 )
    

import time
if __name__ == '__main__':
    n = 35
    t0 = time.time()
    print fibonacci( n )
    time_raw = time.time() - t0 
    t0 = time.time()
    print eternal_cached_fib( n )
    time_eternal_cache = time.time() - t0 
    
    print "raw time (no cache):", time_raw
    print "eternal cache time:", time_eternal_cache
    
    """cache = Memycache()
    cache.add("key", "val")
    print cache.get("key")"""
