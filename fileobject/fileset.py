# -*- coding: utf-8 -*-
import os
import logging
import fnmatch

#%%---------------------------------------------------------------------------#
class FileSet(set):

    #%%-----------------------------------------------------------------------#
    def __new__(cls, *args, **kwargs):
        
        obj = super().__new__(cls)
                        
        obj.logger = logging.Logger(__name__)
        
        return obj
    
    #%%-----------------------------------------------------------------------#
    def __add__(self, other):
        

        return FileSet(self.union(other))

    #%%-----------------------------------------------------------------------#
    def __sub__(self, other):
        
        return FileSet(self.difference(other))
    
    #%%-----------------------------------------------------------------------#
    def load(self, fname):
        
        with open(fname, 'r') as fobj:
            
            paths = [os.path.abspath(p) for p in fobj.read().split('\n') if os.path.lexists(p)]
            
            if not paths:
                
                self.logger.warn('No valid path is loaded.')
            
            self.__init__(paths)
        
            
        return self

    #%%-----------------------------------------------------------------------#    
    def save(self, fname, relative=True):

        with open(fname, 'w') as fobj:
            
            if relative:
                fobj.writelines('\n'.join(sorted(os.path.relpath(p, 
                                    os.path.dirname(fname)) for p in self)))
                
            else:
                fobj.writelines('\n'.join(sorted(self)))
            
        return self
    
    #%%-----------------------------------------------------------------------#    
    def filter(self, *pattern, union=True): 
        
        if union:
            
            return sum((FileSet(fnmatch.filter(self, p)) for 
                        p in pattern), FileSet([]))  
        
        else:
            
            s = self.filter(pattern[0])
            
            for p in pattern[1:]:
                
                s = FileSet(s.intersection(s.filter(p)))

                
            return FileSet(s)
            
        
#%%---------------------------------------------------------------------------#