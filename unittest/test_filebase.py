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

    test_path = r"Y:\\"
    
    print('Test path is "{}".'.format(os.path.abspath(test_path)))
    
    
    
#    fb = FileBase(test_path)
#    fb.save(os.path.join(test_path, '~contents.index'), relative=False)

    fs = FileSet()
    fs.load(os.path.join(test_path, '~contents.index'))
    
    print(fs['*The.Grand.Tour.S03E10.720p.WEB.H264-AMCON*'].basename())
    
    #unittest.main(verbosity=2)
    
    