# -*- coding: utf-8 -*-

import sys
import os

if "../.." not in sys.path:
    sys.path.append("../..")
    

import unittest 
from filebase.fileobject import FileBase, FileList

#%%---------------------------------------------------------------------------#
class Test_FileBase(unittest.TestCase):
    
    def test_init(self):
        '''
        test if a FileBase object is an instance of FileList.
        '''
        
        self.assertIsInstance(fb, FileList)
    
    def test_root_exist(self):
        
        '''
        test if all root of FileBase object exist.
        '''
        
        self.assertTrue(all(os.path.lexists(p) for p in fb.root))
        
        
    #%%-----------------------------------------------------------------------#

#%%---------------------------------------------------------------------------#
    
if __name__ == '__main__':

    test_path = "../.."
    
    print('Test path is "{}".'.format(os.path.abspath(test_path)))
    
    fb = FileBase(test_path)
    
    print(fb.root)
    
    unittest.main(verbosity=2)