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
    
    fv1 = ffs.relpath(root).relpath(0, 1)
    
    _, keys = zip(*fv1.apply(lambda x: x.split('.')[0] if '.' in x else None))
    
    keys = set([k for k in keys if k is not None and len(k)>1])
    
    for k in keys:
        
        tempdir = os.path.join(root, '_temp')
        dstdir = os.path.join(root, k)

        if not os.path.lexists(tempdir):
            
            os.mkdir(tempdir)     
            
        found = ffs.relpath(root).relpath(0, 1)['*{}*'.format(k)]
        
        if len(found)<=1:
            continue
        ans = input('{} {}'.format(k, len(found)))
        if ans == 'y':
            
            
            print((found))

            
            try:
                found.joindir(root).apply(shutil.move, tempdir)
                os.rename(tempdir, dstdir)
            except:
                pass
            
            
            

        if ans == 'end':
            
            break
        
def sort_file2():

    fb = FileBase(root)
    fb.save(os.path.join(root, '~contents.all.filebase'), relative=True)

    fs = FileSet().load(os.path.join(root, '~contents.all.filebase'))
    
    fs.dirs.save(os.path.join(root, '~contents.dirs.filebase'))
    fs.files.save(os.path.join(root, '~contents.files.filebase'))
    
    ffs = FileSet().load(os.path.join(root, '~contents.files.filebase'))
    dfs = FileSet().load(os.path.join(root, '~contents.dirs.filebase'))
    

    
    sortroot = os.path.normpath(r"Z:\\_new_incoming")
    sortdirs = {
            0: '人工',
            1: '东方古典',
            2: '中文流行',
            3: '儿童',
            4: '卡拉OK',
            5: '原声',
            6: '外文流行',
            7: '西方古典',
            8: '试音宝典',
            9: '轻音乐',
            }

    
    lv1 = ffs.relpath(root).relpath(0, 1).joindir(root)
    
    while 1:
        k = lv1.pop()
        
        if not os.path.lexists(k):
            continue
        
        ans = input('{}: '.format(k))
        
        if ans == '':
            
            continue
        
        if ans == 'end' :
            ffs.save(os.path.join(root, '~contents.files.filebase'))
            break
        
        else: 
            
            select = ans
    
        
        targetdir = os.path.join(sortroot, sortdirs[int(select)])
        if not os.path.lexists(targetdir):
            os.mkdir(targetdir)
        
        ans = input('{}?  '.format(targetdir))
        
        if ans == 'end':
            ffs.save(os.path.join(root, '~contents.files.filebase'))
            break
        
        elif ans == 'y':
            
            try:
        
                shutil.move(k, targetdir)
                
            except Exception as err:
                
                ffs.logger.warn(str(err))
                
            else:
                
                pass
#%%---------------------------------------------------------------------------#

   
if __name__ == '__main__':

    root = os.path.normpath(r"Z:\轻音乐\_unsorted")
    
    print('Test path is "{}".'.format(os.path.abspath(root)))
    
    fb = FileBase(root)
    fb.save(os.path.join(root, '~contents.all.filebase'))

#    fs = FileSet().load(os.path.join(root, '~contents.all.filebase'))
    
    dfs = fb.dirs
    
    
    dfs.save(os.path.join(root, '~contents.dirs.filebase'))
    (fb-dfs).save(os.path.join(root, '~contents.files.filebase'))
    
    
    afs = FileSet().load(os.path.join(root, '~contents.all.filebase'))
    ffs = FileSet().load(os.path.join(root, '~contents.files.filebase'))
    dfs = FileSet().load(os.path.join(root, '~contents.dirs.filebase')) 
    
    
#    for f in ffs['*(1)*']:
#        
#        twin = f.replace('(1)', '')
#        
#        if os.path.lexists(twin) and os.path.getsize(f) == os.path.getsize(twin):
#            
#            os.remove(f)
            
            
        

#    print(dfs.find_empty().apply(os.rmdir))
    
#    for d, d1 in afs.squeeze_dir(dfs, ffs):
#
#        if os.path.basename(d) == os.path.basename(d1):
#            
#            d1fs = afs[d1+os.sep+'*']
#            d1fs.apply(shutil.move, d)
        

    
#    d = 'Z:\\轻音乐\\unzip\\New Age Style - Vocal New Age Hits 1 (2013)'
#
#    d1, = dfs[d+os.sep+'*']
#    
#    print(len(ffs[d+os.sep+'*']), len(ffs[d1+os.sep+'*']))
        


    
