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
            
        
        items = sum((FileSet(FileBase.list_files(rt, depth=depth
                                )) for rt in self.root), FileSet([]))
        
        self._files = FileSet(p for p in items if not p.endswith(os.sep))
        
        super().__init__(os.path.normpath(p) for p in items)
        
        self._dirs = self - self._files
        
        if kind == 'file':
            
            super().__init__(self._files)
        
        elif kind == 'dir':
            super().__init__(self._dirs)
                    
    #%%-----------------------------------------------------------------------#
    @staticmethod
    def list_files(root, *, depth=None):
        
        '''
        list all files in the root folder.
        
        depth: depth of the folder structure, if None, will scan to deepest folder
        '''
        

        
        for rt, dirs, files in os.walk(root):
            
            d = len(os.path.relpath(rt, root).split(os.sep))
            
            if d > depth:
                
                del dirs[:]
                
                continue
       
            if rt != root: 
                
                yield rt + os.sep
            

            for f in files:
                
                yield os.path.join(rt, f)
            

            
    #%%-----------------------------------------------------------------------#
      
#%%---------------------------------------------------------------------------#