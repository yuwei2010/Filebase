# -*- coding: utf-8 -*-

import os
import logging
from filebase.fileobject import FileSet

#%%---------------------------------------------------------------------------#
class FileBase(FileSet):
    
    indexfile = '~$indices.filebase'        
    filterlist = ['~$*'] 
    
    #%%-----------------------------------------------------------------------#    
    def __init__(self, *root, depth=None, kind='all'):
        
        if not root:
            
            self.root = (os.getcwd(),)
            
        else:
            
            self.root = tuple(set([os.path.abspath(p) for p in root]))
            
        
        super().__init__(sum((FileSet(FileBase.list_files(rt, depth=depth, 
             kind=kind)) for rt in self.root), FileSet([])))
        
            
    #%%-----------------------------------------------------------------------#
    @staticmethod
    def list_files(root, *, depth=None, kind='all'):
        
        '''
        list all files in the root folder.
        
        depth: depth of the folder structure, if None, will scan to deepest folder
        '''
        
        count = 0
        
        for rt, dirs, files in os.walk(root):
            
            if depth is not None and count > depth:
                break
            

            if rt != root and kind == 'all' or kind == 'dir':               
                yield rt
            
            if kind == 'all' or kind == 'file':
                for f in files:
                    
                    yield os.path.join(rt, f)
            
            count += 1
            
    #%%-----------------------------------------------------------------------#
      
#%%---------------------------------------------------------------------------#