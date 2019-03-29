# -*- coding: utf-8 -*-

import sys
import os

if "../.." not in sys.path:
    sys.path.append("../..")
    

import unittest 
import shutil
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

    test_path = os.path.normpath(r"Y:/")
    
    print('Test path is "{}".'.format(os.path.abspath(test_path)))
    
    
    
#    fb = FileBase(test_path)
#    fb.save(os.path.join(test_path, '~contents.index'), relative=True)

    fs = FileSet().load(os.path.join(test_path, '~contents.index'))
    
    print(fs.exts)
    
    fs['*.mkv'].save(os.path.join(test_path, '~contents.mkv.filebase'))
    
    ds = fs['*.mkv'].dirname()-FileSet([test_path])
    
    print(ds.apply(shutil.move, os.path.join(test_path, '_TMP')))
    
