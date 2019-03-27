# -*- coding: utf-8 -*-
import os
import io
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
    def __getitem__(self, s):
        
        return self.filter(s)
    #%%-----------------------------------------------------------------------#
    def basename(self):
        
        return {os.path.basename(p) for p in self}
    #%%-----------------------------------------------------------------------#
    def commonpath(self):
        
        return os.path.commonpath(self)
    #%%-----------------------------------------------------------------------#
    def isabs(self):
        
        return dict((p, os.path.isabs(p)) for p in self)
    
    #%%-----------------------------------------------------------------------#
    def load(self, fname):
        
        with io.open(fname, "r", encoding="utf-8") as fobj:
            
            paths = [os.path.abspath(p) for p in fobj.read().split('\n')]
                        
            self.__init__(paths)
        
            
        return self

    #%%-----------------------------------------------------------------------#    
    def save(self, fname, relative=True):
        
        
        with io.open(fname, "w", encoding="utf-8") as fobj:
            
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