'''
Created on 12. apr. 2014

@author: Kim-Georg Aase
'''

import time
import operator

import collections
import functools



class CacheObject( object ):
    def __init__( self, data ):
        self.data = data
        self.timestamp = None    
        self.setTimestamp()
    
    def setTimestamp( self ):
        # TODO: ??? chose between time or clock, or????
        self.timestamp = time.time()
        
    def is_valid( self, duration ):
        if not duration:
            return True
        if ( time.time() - self.timestamp ) > duration:
            return False
        else:
            return True

class Memycache( object ):
    """
        ??? How to - faster deletion on timestamp???
    """
    def __init__( self, max_size = 100000, duration = None ):
        
        self.max_size = max_size
        self.duration = duration
        
        self.cache = {}
        
    
    def __call__( self, func ):
        def wrapped_func( *args, **kwargs ):
            key = str( func ) + str( args ) + str( kwargs )
            if not isinstance( args, collections.Hashable ):
                # uncacheable. a list, for instance.
                # better to not cache than blow up.
                return func( *args, **kwargs )
            
            val = self.get( key )
            if val: 
                return val
            
            val = func( *args, **kwargs )
            self.add( key, val )
            return val
        return wrapped_func
        
    """def __repr__(self):
        '''Return the function's docstring.'''
        return self.func.__doc__
    
    def __get__(self, obj, objtype):
        '''Support instance methods.'''
        return functools.partial(self.__call__, obj)"""
        
    
    def _remove_old( self ):
        removed = False
        if self.duration:
            for key, val in self.cache.items():
                if not val.is_valid():
                    del self.cache[key]
                    removed = True
        if removed:
            return
        
        count = 0
        nr_of_delations = len( self.cache ) * 0.25
        for i in sorted( self.cache.keys(), key = lambda obj: self.cache[obj].timestamp ):
            if count < nr_of_delations:
                del self.cache[i]
                count += 1
            else:
                break
    
    def add( self, key, val, overwrite = False ):
        if len( self.cache ) >= self.max_size and self.max_size > 0:
            self._remove_old()
            
        if key in self.cache:
            if self.cache[key].data == val:
                self.cache[key].setTimestamp()
            elif overwrite:
                self.cache[key] = CacheObject( val )
        else:
            self.cache[key] = CacheObject( val )
    
    def get( self, key ):
        obj = self.cache.get( key )
        if not obj:
            return
        if not obj.is_valid( self.duration ):
            del self.cache[key]
            return
        obj.setTimestamp()
        return obj.data
    

class Eternal( Memycache ):
    def __init__( self, func ):
        super( Eternal, self ).__init__( 0, None )
        self.func = func
        
    def __call__( self, *args ):
        key = str( self.func ) + str( args )
        if not isinstance( args, collections.Hashable ):
            # uncacheable. a list, for instance.
            # better to not cache than blow up.
            return self.func( *args )
        
        val = self.get( key )
        if val: 
            return val
        
        val = self.func( *args )
        self.add( key, val )
        return val


    
    
    
    
    
    
    
