# -*- coding: utf-8 -*-

import os
import logging
from filebase.fileobject import FileList

#%%---------------------------------------------------------------------------#
class FileBase(FileList):
    
    indexfile = '~$indices.filebase'        
    filterlist = ['~$*'] 
    
    #%%-----------------------------------------------------------------------#    
    def __init__(self, *root):
        
        if not root:
            
            self.root = (os.getcwd(),)
            
        else:
            
            self.root = tuple(set([os.path.abspath(p) for p in root]))
            
        
            
    #%%-----------------------------------------------------------------------#
    @staticmethod
    def list_files(root, *, depth=None):
        
        '''
        list all files in the root folder.
        
        depth: 
        '''
        
        count = 0
        
        for rt, dirs, files in os.walk(root):
            
            if depth and count > depth:
                break
            
            for f in files:
                print(os.path.normpath(os.path.join(rt, f)))
            
            depth += 1
            
        
#%%---------------------------------------------------------------------------#