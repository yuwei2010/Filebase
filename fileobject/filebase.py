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
        
        count = 0
        
        for rt, dirs, files in os.walk(root):
            
            if depth and count > depth:
                break
            
            
            
            depth += 1
            
        
#%%---------------------------------------------------------------------------#