# -*- coding: utf-8 -*-
import os
import io
import logging
import fnmatch

from datetime import date


#%%---------------------------------------------------------------------------#
def getpath(p):
    
    if hasattr(p, 'path'):
        
        return p.path
    else:
        return p
#%%---------------------------------------------------------------------------#
class FileStr(str):

    #%%-----------------------------------------------------------------------#
    def __new__(cls, s, path=None):
        
        obj = super().__new__(cls, s)
        
        obj.path = s if path is None else path
        
        return obj    
    
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

    def exts(self):
        
        return set(list(zip(*self.splitext()))[-1]) - set([''])
    #%%-----------------------------------------------------------------------#    

    def files(self):
        if hasattr(self, '_files'):
            
            return self._files

        return FileSet(p for p in self if os.path.isfile(p))        
    #%%-----------------------------------------------------------------------#    

    def dirs(self):

        if hasattr(self, '_dirs'):
            
            return self._dirs        
        return FileSet(p for p in self if os.path.isdir(p)) 
    
    #%%-----------------------------------------------------------------------#    

    def items(self):
        
        return FileSet(p for p in self if os.path.lexists(p))
    #%%-----------------------------------------------------------------------#
    def copy(self):
        
        return FileSet(super().copy())
    
    #%%-----------------------------------------------------------------------#
    def fcount(self, sep=' ', fmt=lambda x:x):
        
        from collections import Counter
        lst = []
        

        for p in self:
            for s in os.sep+sep:
            
                p = p.replace(s, ' ')
            
            lst.extend(fmt(p).split())
            
        return Counter(lst)
    
    #%%-----------------------------------------------------------------------#
    def count(self, *strs):
        
        if not strs:
            
            return len(self)
        
        return [(s, len(self['*{}*'.format(s)])) for s in strs]
        
    #%%-----------------------------------------------------------------------#
    def iterapply(self, func, *args, **kwargs):
        
        for p in self:
            
            try:
                yield (p, func(p, *args, **kwargs))
            except Exception as err:
                self.logger.warn(str(err))
        

    #%%-----------------------------------------------------------------------#
    def apply(self, func, *args, **kwargs):    
        
        return list(self.iterapply(func, *args, **kwargs))
    #%%-----------------------------------------------------------------------#
    def basename(self):
        
        return FileSet(FileStr(os.path.basename(p), getpath(p)) for p in self)
    
    #%%-----------------------------------------------------------------------#
    def commonpath(self):
        
        return os.path.commonpath(self)
    
    #%%-----------------------------------------------------------------------#
    def dirname(self):
        
        return FileSet(os.path.dirname(p) for p in self)

    #%%-----------------------------------------------------------------------#
    def diffmatch(self, pattern, gauge=0.5):
        
        from difflib import SequenceMatcher
        return FileSet(p for p in self if SequenceMatcher(None, pattern, p).ratio() >= gauge)
    #%%-----------------------------------------------------------------------#
    def distance(self, pattern):
        
        import nltk
        

        return list(zip(*sorted((nltk.edit_distance(pattern, p), p) for p in self)))[1]
    
    #%%-----------------------------------------------------------------------#
    def endswith(self, s):
        
        return FileSet(p for p in self if p.endswith(s))
    #%%-----------------------------------------------------------------------#
    def exist(self):
        
        return [(p, os.path.exists(p)) for p in self]
    #%%-----------------------------------------------------------------------#
    def find_empty(self):
        
        return FileSet(d for d in self if os.path.isdir(d) and not os.listdir(d))
    #%%-----------------------------------------------------------------------#
    def getatime(self):
        
        return [(p, date.fromtimestamp(os.path.getatime(p))) for p in self]
    #%%-----------------------------------------------------------------------#
    def getmtime(self):
        
        return [(p, date.fromtimestamp(os.path.getmtime(p))) for p in self]
    #%%-----------------------------------------------------------------------#
    def getctime(self):
        
        return [(p, date.fromtimestamp(os.path.getctime(p))) for p in self]
    #%%-----------------------------------------------------------------------#
    def getsize(self):
        
        return [(p, os.path.getsize(p)) for p in self]
    
    #%%-----------------------------------------------------------------------#
    def groupby(self, func):
        
        retdict = dict()
        
        for p in self:
            
            retdict.setdefault(func(p), FileSet()).add(p)
            
        return retdict
    #%%-----------------------------------------------------------------------#
    def isabs(self):
        
        return [(p, os.path.isabs(p)) for p in self]
    #%%-----------------------------------------------------------------------#
    def joinfile(self, fname):
        
        return FileSet(os.path.join(p, os.path.normpath(fname)) for p in fname)
    #%%-----------------------------------------------------------------------#
    def joindir(self, dname):
        
        return FileSet(os.path.join(os.path.normpath(dname), p) for p in self)
    #%%-----------------------------------------------------------------------#
    def joinext(self, ext=None):
        
        if ext is None:
            
            return FileSet(p for p, _ in self.splitext())
        else:
            return FileSet(p+ext for p, _ in self.splitext())
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
    def relpath(self, start=os.curdir, end=None):
        
        if isinstance(start, str):
        
            return FileSet(FileStr(os.path.relpath(p, start), getpath(p)) for p in self)
        else:
            
            s = slice(start, end)
            
            return FileSet(FileStr(os.sep.join(p.split(os.sep)[s]), getpath(p)) for 
                           p in self).remove('')
    #%%-----------------------------------------------------------------------#
    @classmethod
    def squeeze_dir(self, dirs=None, files=None):
        
        files = self.files if files is None else files
        dirs = self.dirs if dirs is None else dirs
        
        for d in dirs:
            
            try:
                d1, = dirs[d+os.sep+'*']
            except:
                continue
            
            if len(files[d+os.sep+'*']) == len(files[d1+os.sep+'*']):
                
                yield d, d1
            
    #%%-----------------------------------------------------------------------#
    def split(self):   
        
        return [os.path.split(p) for p in self]
    
    #%%-----------------------------------------------------------------------#
    def splitext(self):
        
        return [(os.path.splitext(p)) for p in self]
    #%%-----------------------------------------------------------------------#
    def startswith(self, s):
        
        return FileSet(p for p in self if p.startswith(s))

    #%%-----------------------------------------------------------------------#
    def pop(self, *s):
        if not s:
            
            return super().pop()
        else:
            other = FileSet(s)
            
            self.__init__(self-other)
            
            return other
    
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
    def remove(self, *s):
        other = FileSet(s)
        
        self.__init__(self-other)
        
        return self
    #%%-----------------------------------------------------------------------#
    def relpath2(self, root, level=None):
        
        return self.relpath(root).relpath(0, level).joindir(root)
    #%%-----------------------------------------------------------------------#
    def load(self, fname, relative=True, check=False):
        
        with io.open(fname, "r", encoding="utf-8") as fobj:
            
            if relative:
            
                paths = (os.path.normpath(os.path.join(os.path.dirname(fname), p)) for 
                         p in fobj.read().split('\n') 
                         if p.strip() and not p.strip().startswith('#'))
            else:
                
                paths = (os.path.normpath(p) for p in fobj.read().split('\n') 
                         if p.strip() and not p.strip().startswith('#'))
                                 
            if check:
                
                paths = (p for p in paths if os.path.lexists(p))
            
            self.__init__(paths)
        
            
        return self
    #%%-----------------------------------------------------------------------#    
    def take(self, start=None, end=None, step=None):
        
        s = slice(start, end, step)
        return FileSet(sorted(self)[s])
    #%%-----------------------------------------------------------------------#    
    def save(self, fname, relative=True):
        
        
        with io.open(fname, "w", encoding="utf-8") as fobj:
            
            if relative:
                
                start = os.path.dirname(fname)
                fobj.writelines('\n'.join(sorted(os.path.relpath(p, 
                                    start) for p in self)))
                
            else:
                fobj.writelines('\n'.join(sorted(self)))
            
        return self

    #%%-----------------------------------------------------------------------#  
    def abspath(self):
                
        return FileSet(FileStr(getpath(p)) for p in self)
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
            
    #%%-----------------------------------------------------------------------#   
    def match(self, pattern):

        import re

        patt = re.compile(pattern)   
        
        return FileSet(p for p in self if patt.match(p) is not None) 
#%%---------------------------------------------------------------------------#