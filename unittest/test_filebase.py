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


def sort_file1():
    
    fv1 = ffs.relpath(test_path).relpath(0, 1)
    
    _, keys = zip(*fv1.apply(lambda x: x.split('.')[0] if '.' in x else None))
    
    keys = set([k for k in keys if k is not None and len(k)>1])
    
    for k in keys:
        
        tempdir = os.path.join(test_path, '_temp')
        dstdir = os.path.join(test_path, k)

        if not os.path.lexists(tempdir):
            
            os.mkdir(tempdir)     
            
        found = ffs.relpath(test_path).relpath(0, 1)['*{}*'.format(k)]
        
        if len(found)<=1:
            continue
        ans = input('{} {}'.format(k, len(found)))
        if ans == 'y':
            
            
            print((found))

            
            try:
                found.joindir(test_path).apply(shutil.move, tempdir)
                os.rename(tempdir, dstdir)
            except:
                pass
            
            
            

        if ans == 'end':
            
            break
#%%---------------------------------------------------------------------------#

   
if __name__ == '__main__':

    test_path = os.path.normpath(r"Z:\中文流行")
    
    print('Test path is "{}".'.format(os.path.abspath(test_path)))
    
    
    
    
#    fb = FileBase(test_path)
#    fb.save(os.path.join(test_path, '~contents.all.filebase'), relative=True)
#
#    fs = FileSet().load(os.path.join(test_path, '~contents.all.filebase'))
#    
#    fs.dirs.save(os.path.join(test_path, '~contents.dirs.filebase'))
#    fs.files.save(os.path.join(test_path, '~contents.files.filebase'))
    
    ffs = FileSet().load(os.path.join(test_path, '~contents.files.filebase'))
    dfs = FileSet().load(os.path.join(test_path, '~contents.dirs.filebase'))
    
    tempdir = os.path.join(test_path, '_unsorted')


    if not os.path.lexists(tempdir):
        
        os.mkdir(tempdir) 

    
    lv1 = ffs.relpath(test_path).relpath(0, 1)
    
    print(dfs.get_emptydir().apply(os.rmdir))
    
#    FileSet([p for p in lv1 if len(p)>3]).joindir(test_path).apply(shutil.move, tempdir)
    


    
    

    
