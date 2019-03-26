# -*- coding: utf-8 -*-

import sys
import os

if "../.." not in sys.path:
    sys.path.append("../..")
    

import unittest 
from filebase.fileobject import FileBase, FileSet

#%%---------------------------------------------------------------------------#
class Test_FileBase(unittest.TestCase):
    
    def test_init(self):
        '''
        test if a FileBase object is an instance of FileList.
        '''
        
        self.assertIsInstance(fb, FileSet)
    

        
        
    #%%-----------------------------------------------------------------------#

#%%---------------------------------------------------------------------------#

   
if __name__ == '__main__':

    test_path = ".."
    
    print('Test path is "{}".'.format(os.path.abspath(test_path)))
    
    
    fs = FileSet()
    fb = FileBase(test_path)
    
    
    fb.save(os.path.abspath('indices.txt'))
    
    fs.load('indices.txt')
    
    
    print(fs.filter('*fileobject*', '*.py', union=False))
#    print(fs)
    
    unittest.main(verbosity=2)
    
    