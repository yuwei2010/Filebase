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
    @property
    def exts(self):
        
        return set(list(zip(*self.splitext()))[-1])
    #%%-----------------------------------------------------------------------#
    def iterapply(self, func, *args, **kwargs):
        
        return ((p, func(p, *args, **kwargs)) for p in self)
    #%%-----------------------------------------------------------------------#
    def apply(self, func, *args, **kwargs):    
        
        return list(self.iterapply(func, *args, **kwargs))
    #%%-----------------------------------------------------------------------#
    def basename(self):
        
        return {os.path.basename(p) for p in self}
    
    #%%-----------------------------------------------------------------------#
    def commonpath(self):
        
        return os.path.commonpath(self)
    
    #%%-----------------------------------------------------------------------#
    def dirname(self):
        
        return FileSet(os.path.dirname(p) for p in self)
    
    #%%-----------------------------------------------------------------------#
    def exist(self):
        
        return [(p, os.path.exists(p)) for p in self]
    #%%-----------------------------------------------------------------------#
    def getsize(self):
        
        return [(p, os.path.getsize(p)) for p in self]
    #%%-----------------------------------------------------------------------#
    def isabs(self):
        
        return [(p, os.path.isabs(p)) for p in self]
    #%%-----------------------------------------------------------------------#
    def joinfile(self, fname):
        
        return FileSet(os.path.join(p, fname) for p in fname)
    #%%-----------------------------------------------------------------------#
    def joindir(self, dname):
        
        return FileSet(os.path.join(dname, p) for p in self.basename())
    #%%-----------------------------------------------------------------------#
    def lexist(self):
        
        return [(p, os.path.lexists(p)) for p in self]  
    #%%-----------------------------------------------------------------------#
    def normpath(self):
        
        return FileSet(os.path.normpath(p) for p in self)
    #%%-----------------------------------------------------------------------#
    def realpath(self):
        
        return FileSet(p for p in self)
    #%%-----------------------------------------------------------------------#
    def relpath(self, start=os.curdir):
        
        return FileSet(os.path.relpath(p, start) for p in self)
    #%%-----------------------------------------------------------------------#
    def split(self):   
        
        return [os.path.split(p) for p in self]
    
    #%%-----------------------------------------------------------------------#
    def splitext(self):
        
        return [(os.path.splitext(p)) for p in self]
    #%%-----------------------------------------------------------------------#
    def popen(self, cmd):
        
        import subprocess
        
        def call(p):
            
            _cmd = cmd.format(p) 
            
            proc = subprocess.Popen(_cmd, stdout=subprocess.PIPE, shell=True, )
            stdout, _ = proc.communicate()
            
            return stdout
        
        return [(p, call(p)) for p in self]
        
 
    #%%-----------------------------------------------------------------------#
    def load(self, fname, relative=True):
        
        with io.open(fname, "r", encoding="utf-8") as fobj:
            
            if relative:
            
                paths = (os.path.normpath(os.path.join(os.path.dirname(fname), p)) for 
                         p in fobj.read().split('\n'))
            else:
                
                paths =  (os.path.normpath(p) for p in fobj.read().split('\n'))
                        
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