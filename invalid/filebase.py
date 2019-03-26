# -*- coding: utf-8 -*-
import re
import os
import fnmatch
import functools
import logging

from .tools import mproperty

byte_pattern = re.compile(r'([0-9eE.]+)([ bkmgt]+)', re.I)


#%%---------------------------------------------------------------------------#
class ByteInt(int):
    
    decimals = 3
            
    factors = {'B': 1, 'KB': 1e3, 'MB': 1e6, 'GB': 1e9, 'TB': 1e12,
               'K': 1e3, 'M': 1e6, 'G': 1e9, 'T': 1e12}

    #%%-----------------------------------------------------------------------#        
    def __new__(cls, s, decimals=None):
        
        if isinstance(s, str):
            
            (value, unit), = byte_pattern.findall(s.strip())
            
            s = float(value) * ByteInt.factors[unit.strip().upper()]
        
        obj = super().__new__(cls, s)

        obj.decimals = ByteInt.decimals if decimals is None else decimals

        obj.str = '{{:0.{}f}}'.format(int(obj.decimals))
        
        return obj
    
    #%%-----------------------------------------------------------------------#    
    def __str__(self):
        
        b = int(self)
        s = str(b)
        l = len(s)
        
        if l <= 3:
            
            bystr = '{} Byte'.format(b)
            
        elif l <= 6:
            
            bystr = '{} KB'.format(self.str.format(b / 1e3))
            
        elif l <= 9:
            
            bystr = '{} MB'.format(self.str.format(b / 1e6))
            
        elif l <= 12:
            
            bystr = '{} GB'.format(self.str.format(b / 1e9))

        else:
            
            bystr = '{} TB'.format(self.str.format(b / 1e12))
            
        return bystr  

    __repr__ = __str__ 

    #%%-----------------------------------------------------------------------#    
    def __add__(self, other):
        
        return ByteInt(super().__add__(ByteInt(other)), decimals=self.decimals)
    
    __iadd__ = __add__
    
    #%%-----------------------------------------------------------------------#    
    def __sub__(self, other):
        
        return ByteInt(super().__sub__(ByteInt(other)), decimals=self.decimals)
    
    __isub__ = __sub__

    #%%-----------------------------------------------------------------------#
    def __mul__(self, other):
        
        return ByteInt(super().__mul__(ByteInt(other)), decimals=self.decimals)
    
    __imul__ = __mul__   
    
    #%%-----------------------------------------------------------------------#
    def __truediv__(self, other):
        
        return ByteInt(super().__truediv__(ByteInt(other)), decimals=self.decimals)
    
    __idiv__ = __truediv__
    
    #%%-----------------------------------------------------------------------#
    def __mode__(self, other):
        
        return ByteInt(super().__mode__(other), decimals=self.decimals)
    
    __imode__ = __mode__ 
    
#%%---------------------------------------------------------------------------#
class FileItem(str):
    
    def __new__(cls, s, root, method):
        
        obj = super().__new__(cls, os.path.join(root, s))
        obj.method = method
        obj.root = root
        obj.symlink = os.path.basename(root)
        obj.flatted = False
                
        return obj
   
    #%%-----------------------------------------------------------------------#
    def __int__(self):
        
        return self.byte
    
    __float__ = __int__

    #%%-----------------------------------------------------------------------#
    @mproperty
    def name(self):
        
        return os.path.relpath(self, self.root)

    #%%-----------------------------------------------------------------------#
    @mproperty
    def basename(self):
        
        return os.path.basename(self)
    
    #%%-----------------------------------------------------------------------#
    @mproperty
    def forename(self):
        
        return os.path.splitext(self.basename)[0] 

    #%%-----------------------------------------------------------------------#
    @mproperty
    def path_prefix(self):
        
        return os.sep.join([self.pardir, self.forename])
    
    #%%-----------------------------------------------------------------------#
    @mproperty
    def ext(self):
        
        return os.path.splitext(self.basename)[-1]

    #%%-----------------------------------------------------------------------#
    @mproperty
    def path(self):
        
        return str(self)
    
    #%%-----------------------------------------------------------------------#
    @mproperty
    def sympath(self):
        
        if self.flatted:            
            return os.path.join(self.symlink, self.basename)
        else:
            return os.path.join(self.symlink, self.name)
    
    #%%-----------------------------------------------------------------------#
    @mproperty
    def pardir(self):
        
        return os.path.dirname(self.path)
    
    #%%-----------------------------------------------------------------------#
    @mproperty
    def dirname(self):
        
        return os.path.basename(self.pardir)  
    
    #%%-----------------------------------------------------------------------#
    @mproperty
    def subroot(self):
        
        parts = os.path.normpath(self.name).split(os.sep)
        
        if len(parts) > 1:
            
            return os.path.join(self.root, parts[0])
        
        else:
            
            return self.root
           
    #%%-----------------------------------------------------------------------#
    @property
    def value(self):
        
        assert self.exists()
        
        if hasattr(self.method, '__call__'):
            
            return self.method(self)
        
        else:
        
            raise IOError('No opening method defined for "{}"'.format(self))

    #%%-----------------------------------------------------------------------#
    @mproperty
    def byte(self):
        
        return ByteInt(os.path.getsize(self.path))
    
    #%%-----------------------------------------------------------------------#
    def exists(self):
        
        return os.path.isfile(self.path)
    
    #%%-----------------------------------------------------------------------#
    def copy(self, clean=False):
        
        item = FileItem(self, self.root, self.method)
        
        if not clean:
            item.symlink = self.symlink
            item.flatted = self.flatted
        
        return item 
    
    #%%-----------------------------------------------------------------------#
    def with_suffix(self, ext='', method=None):
        
        ext = ext.strip()
        ext = ext if ext.startswith('.') else '.' + ext if ext else ext
        
        return FileItem(os.path.splitext(self)[0] + ext, root=self.root, method=method)
    
    #%%-----------------------------------------------------------------------#
    def with_name(self, name='', method=None):
        
        return FileItem(os.path.join(self.pardir, name.strip()), root=self.root, method=method)  
         
    #%%-----------------------------------------------------------------------#
    def openwith(self, method=None, arg=None, kwargs=None):
        
        arg = tuple() if arg is None else arg
        kwargs = dict() if kwargs is None else kwargs
        
        if method is not None:
            fun = lambda f, arg=arg, kwargs=kwargs: method(f, *arg, **kwargs)
            
            self.method = fun
        else:
            self.method = None
            
        return self
            
#%%---------------------------------------------------------------------------#
class FileList(list):

    #%%-----------------------------------------------------------------------#
    def __new__(cls, *args, **kwargs):
        
        obj = super().__new__(cls)
        
        for attr in ['root', 'name', 'pardir', 'path', 'ext', 'basename', 'dirname', 
                     'byte', 'subroot', 'sympath', 'forename', 'method']:
            
            setattr(obj, attr + 's', lambda attr=attr: 
                                        [getattr(item, attr) for item in obj])
                
        obj.logger = logging.Logger(__name__)
        return obj
    
    #%%-----------------------------------------------------------------------#
    def __init__(self, files, root=None, method=None):
        
        if files is None:
            files = []
                        
        super().__init__(f if isinstance(f, FileItem) else 
                 FileItem(f, root=root, method=method) for f in files)
                                
    #%%-----------------------------------------------------------------------# 
    def check_other(func):
        
        @functools.wraps(func)
        def wrapper(self, other, **kwargs):
            
            if isinstance(other, FileItem):
                
                other = FileList([other]) 
                                
            return func(self, other, **kwargs)
        
        return wrapper
            
    #%%-----------------------------------------------------------------------#
    @check_other
    def __add__(self, other):
        
        if isinstance(other, str) and other.strip().startswith('.'):
            
            return self.twin(other)

        return FileList(sorted(set(super().__add__(other))))
    
    __or__ = __add__
    
    #%%-----------------------------------------------------------------------#
    @check_other
    def __sub__(self, other):
        
        return FileList(sorted(set(self) - set(other)))
    
    #%%-----------------------------------------------------------------------#
    def __truediv__(self, other):
        
        if isinstance(other, str):
            
            other = os.path.normpath(other.strip())
            if not other.startswith(os.path.sep):
                other = os.path.sep + other
            
            if any(s in other for s in '*?'):

                return self.__getitem__('*' + other)
            else:

                return FileList((item for item in self if (item.endswith(other) 
                                    or (other + os.path.sep) in item)))
            
        elif hasattr(other, '__iter__'):
            
            return sum((self.__truediv__(s) for s in other),  FileList([]))
    
    #%%-----------------------------------------------------------------------#
    @check_other
    def __and__(self, other):
        
        return FileList(set(self) & set(other))
            
    #%%-----------------------------------------------------------------------#
    def __getitem__(self, s):
        
        if isinstance(s, FileItem):
            
            return self.__getitem__('*' + s.basename)
        
        elif isinstance(s, str):
            
            s = s.strip()
            
            if s.endswith('/'):
                
                if s.startswith('>'):
                    return FileList(item for item in self if 
                            item.name.count(os.path.sep) + 1 >= s.count('/'))

                elif s.startswith('<'):
                    return FileList(item for item in self if 
                            item.name.count(os.path.sep) + 1 <= s.count('/'))
                else:
                    return FileList(item for item in self if 
                            item.name.count(os.path.sep) + 1 == s.count('/'))
            else:
            
                return FileList(fnmatch.filter(self, s))
            
        elif s is Ellipsis:
            
            return self
        
        elif isinstance(s, type(byte_pattern)):
            
            return FileList([item for item in self if s.match(item)])
        
        elif isinstance(s, (list, tuple)) or hasattr(s, '__iter__'):
                        
            if all(isinstance(ss, bool) for ss in s):
                
                assert len(s) == len(self)
                
                return FileList([item for mask, item in zip(s, self) if mask])
            
            else:
                
                res = list()
                
                for ss in s:
                    
                    item = self.__getitem__(ss)
                    
                    if isinstance(item, list):
                        
                        res.extend(item)
                    
                    else:
                        
                        res.append(item)
                
                return FileList(res)
            
        elif s is None:
            
            return FileList(None)
        
        else:
            
            item = super().__getitem__(s)
            
            if isinstance(item, FileItem):
                
                return item
            
            elif isinstance(item, list):
                
                return FileList(item)
            
    #%%-----------------------------------------------------------------------#
    def __lt__(self, other):

        return FileList(item for item in self if item.byte < ByteInt(other))
    
    #%%-----------------------------------------------------------------------#
    def __le__(self, other):

        return FileList(item for item in self if item.byte <= ByteInt(other))

    #%%-----------------------------------------------------------------------#
    def __gt__(self, other):

        return FileList(item for item in self if item.byte > ByteInt(other))
    
    #%%-----------------------------------------------------------------------#
    def __ge__(self, other):

        return FileList(item for item in self if item.byte >= ByteInt(other))

    #%%-----------------------------------------------------------------------#
    def __eq__(self, other):
                    
        return self.__getitem__(other)

    #%%-----------------------------------------------------------------------#
    def __ne__(self, other):
    
        return self - self.__getitem__(other)

    #%%-----------------------------------------------------------------------#
    def __iadd__(self, other):
        
        if isinstance(other, FileItem):
            
            self.append(other)
        
        elif isinstance(other, FileList):
            
            self.extend(other)
        
        return self
    
    #%%-----------------------------------------------------------------------#
    def __isub__(self, other):
        
        if isinstance(other, FileItem):
            
            self.remove(other)
        
        elif isinstance(other, list):
            
            self.__init__(self.__sub__(other))
        
        return self

    #%%-----------------------------------------------------------------------#
    def bytesum(self):

        return ByteInt(sum(self.bytes()))    
    
    #%%-----------------------------------------------------------------------#
    def bytemax(self):
        
        bytes = self.bytes()
        
        return self.__getitem__(bytes.index(max(bytes)))
    
    #%%-----------------------------------------------------------------------#
    def bytemin(self):
        
        bytes = self.bytes()
        
        return self.__getitem__(bytes.index(min(bytes)))
    
    #%%-----------------------------------------------------------------------#
    def bytesort(self):
        
        bytes = self.bytes()
        
        files_copy = self.copy()
        
        lst = FileList([])
        
        for b in sorted(bytes):
            
            idx = bytes.index(b)
            
            bytes.pop(idx)
            
            lst.append(files_copy.pop(idx))
                        
        return lst
    
    #%%-----------------------------------------------------------------------#
    def tree(self, depth=None, byte=False, onlydir=False, 
                               sort=False, symlink=False, space=5):

        tree, count = self.struct(depth=depth, symlink=symlink,
                                      return_count=True)
                                  
        if not tree:
            
            return None
                    
        def yield_branch(branch, shift=0, ondir=onlydir):
            
            items = sorted((branch.items())) if sort else list(branch.items())
            
            for idx, (key, value) in enumerate(items):
                
                if isinstance(value, dict):
                    
                    if shift == 0:
                        line = key
                    else:
                        line = ''.join([(u'\u2502' + ' ' * space) * (shift - 1),
                                        (u'\u255E' + u'\u2550' * space), key])
                    
                    if ondir and byte:
                        
                        sizes, _ = zip(*yield_branch(value, shift=shift+1, ondir=False))
                        
                        bytesum = ByteInt(sum(sizes))                        
                        yield 0, line + ' ({} items, {})'.format(len(sizes), bytesum)
                        
                    else:
                                                
                        yield 0, line + ' ({} items)'.format(len(value))
    
                    yield from yield_branch(value, shift=shift+1, ondir=ondir)
                
                elif not ondir:
                    
                    bystr = '({})'.format(value.byte) if byte else ''
                    byval = value.byte if byte else 0
                    
                    if idx < len(items) - 1:
                   
                        yield byval, ''.join([(u'\u2502' + ' ' * space) * (shift - 1), 
                                       u'\u251C' + u'\u2500' * space, key, ' {}'.format(bystr)])
                    else:
                        
                        yield byval, ''.join([(u'\u2502' + ' ' * space) * (shift - 1), 
                                       u'\u2514' + u'\u2500' * space, key, ' {}'.format(bystr)])                        
       
        _, lines = zip(*yield_branch(tree))
        
        if byte:

            sizes, _ = zip(*yield_branch(tree, ondir=False))
            
            summary = 'Total {} files. {}'.format(count, ByteInt(sum(sizes)))
            
        else:
            summary = 'Total {} files.'.format(count)
            
        lines = list(lines) + [summary]
            
        return '\n'.join(lines)

    #%%-----------------------------------------------------------------------#
    def count(self, depth=None):
        
        def count_subdirs(dict_,  root=''):
            
            items = list(dict_.items())
            diritems = [(k, v) for k, v in items if isinstance(v, dict)]
            
            yield root, len(diritems), len(items) - len(diritems)
                
            
            for k, v in diritems:
                
                yield from count_subdirs(v, os.path.join(root, k))
                    
        tree, = self.struct(depth=depth).values() 
        
        return count_subdirs(tree) 


    #%%-----------------------------------------------------------------------#
    def pop(self, s):

        if isinstance(s, str):

            found = self.__getitem__(s)
        
            self.__init__(self.__sub__(found))

            return found

        else:
            
            return super().pop(s)
                           
    #%%-----------------------------------------------------------------------#
    def copy(self):

        return FileList([item.copy() for item in self])
    
    #%%-----------------------------------------------------------------------#
    def sort(self, *args, **kwargs):
        
        super().sort(*args, **kwargs)
        
        return self
    #%%-----------------------------------------------------------------------#
    def select(self, criterion):
        
        return FileList((item for item in self if criterion(item)))
    
    #%%-----------------------------------------------------------------------#
    def append(self, item):

        assert isinstance(item, FileItem)
        
        if item not in self:

            super().append(item) 
    
    #%%-----------------------------------------------------------------------#  
    def extend(self, flist):
        
        assert isinstance(flist, FileList)
        
        for item in flist:
            
            self.append(item)
                         
    #%%-----------------------------------------------------------------------#
    def openwith(self, method=None, arg=None, kwargs=None):
                
        for item in self:
            
            item.openwith(method, arg=arg, kwargs=kwargs)
            
        return self
   
    #%%-----------------------------------------------------------------------#
    def values(self):
        
        for item in self:
            
            yield item.value
            
    #%%-----------------------------------------------------------------------#
    def keys(self, *keys):
        
        if not keys:
            
            keyitems = [[str(item) for item in self],]
        
        else:
            
            keyitems = [getattr(self, key + 's')() for key in keys]

        for items in zip(*keyitems):
                        
            if len(items) == 1:
                
                items, = items
            
            yield items   
                 
    #%%-----------------------------------------------------------------------#
    def items(self, *keys):
            
        for keys, value in zip(self.keys(*keys), self.values()):
            
            if not isinstance(keys, (list, tuple)):
                keys = [keys]
            
            yield list(keys) + [value]

    #%%-----------------------------------------------------------------------#
    def with_suffix(self, ext='', method=None):
        
        return FileList(item.with_suffix(ext, method=method) for item in self)
    
    #%%-----------------------------------------------------------------------#
    def with_name(self, name='', method=None):
        
        return FileList(item.with_name(name, method=method) for item in self)
    #%%-----------------------------------------------------------------------#
    def exist(self):
        
        return [item.exists() for item in self]
    
    #%%-----------------------------------------------------------------------#
    def struct(self, depth=None, out=None,
                   symlink=False, return_count=False):
            
        tree = dict()
        count = 0
                
        for item in self:
            
            path = item.sympath if symlink else item.name
            parts = os.path.normpath(path).split(os.sep)
            
            if symlink:
                  
                root = os.path.sep
                    
            else:
                
                root = item.root

            if root not in tree:
                
                tree[root] = dict()
            
            branch = tree[root]
           
            d = 0            
            depth_ = len(parts)-1 if depth is None else min(depth, len(parts)-1)
                                       
            for i, key in enumerate(parts):
                
                if 0 <= d < depth_:
            
                    if key not in branch:
                        
                        branch[key] = dict()
                    
                    branch = branch[key]
                    d += 1
                    
                else:
                    
                    k = os.sep.join(parts[i:])
                    
                    if k not in branch:
                        
                        if out is None:
                            branch[k] = item
                        else:
                            branch[k] = getattr(item, out)
                    
                        count += 1
                    break
                
        if return_count:
            
            return tree, count
        
        else:
            return tree
        
    #%%-----------------------------------------------------------------------#
    def set_symlink(self, symlink=''):
                
        symlink = os.path.normpath(symlink)
        
        idxstr = re.findall('\([0-9]+\)', symlink)
        
        for item in self:
            
            parts = item.split(os.path.sep)[:-1]
            
            sym = symlink
            
            for s in idxstr:
                sym = sym.replace(s, parts[int(s[1:-1]) - 1])

            item.symlink = sym
            
        return self
    
    #%%-----------------------------------------------------------------------#
    def flatted(self, b=True):

        for item in self:

            item.flatted = b
            
        return self
    
    #%%-----------------------------------------------------------------------#
    def update(self):
        
        self.__init__([item for item in self if item.exists()])
        
        return self
    
    #%%-----------------------------------------------------------------------#    
    def zip_files(self, name=None, flat=False, mode='w',
                  compression=True, zip64=True, ignore_error=True):
        
        from .tools import zip_file
        
        if name is None:
            
            root, = set(self.roots())
        
            name = root +'.zip'
        
        filename = lambda item: item.name if flat else item.sympath
        
        zipitems = zip(self.paths(), (filename(item) for item in self))
        
        return zip_file(name, zipitems, mode=mode, compression=compression, 
               zip64=zip64, ignore_error=ignore_error)    
        
    #%%-----------------------------------------------------------------------#    
    def copy2dir(self, new_root, delete_old=False):
        
        def copy_items():
            
            for item in self:
                
                old_root = os.path.basename(item.root)
                sympath = item.sympath
                
                if old_root in sympath:
                    new_path = item.sympath.replace(os.path.basename(item.root), new_root)
                    
                else:
                    
                    new_path = os.path.join(new_root, item.sympath)
                                
                if not os.path.isdir(os.path.dirname(new_path)):
                    os.makedirs(os.path.dirname(new_path))
                    
#                elif os.path.lexists(new_path):
#                    
#                    self.logger.warning('"{}" exists and will be overwritten.'.format(new_path))
                
                if delete_old:
                    shutil.move(item.path, new_path)
                else:
                    shutil.copyfile(item.path, new_path)  
                
                yield FileItem(new_path, root=new_root, method=item.method)
            
        
        import shutil
        
        new_root = os.path.abspath(os.path.normpath(new_root))
        
        return FileList(copy_items())
    
    #%%-----------------------------------------------------------------------#    
    def link2dir(self, new_root):

        def link_items():
            
            for item in self:
                
                old_root = os.path.basename(item.root)
                sympath = item.sympath
                
                if old_root in sympath:
                    new_path = item.sympath.replace(os.path.basename(item.root), new_root)
                    
                else:
                    
                    new_path = os.path.join(new_root, item.sympath)
                                
                if not os.path.isdir(os.path.dirname(new_path)):
                    os.makedirs(os.path.dirname(new_path))
                    
                elif os.path.lexists(new_path):
                    
#                    self.logger.warning('"{}" exists and will be overwritten.'.format(new_path))
                    os.remove(new_path)

                os.symlink(item.path, new_path)  
                
                yield FileItem(new_path, root=new_root, method=item.method)
        
        new_root = os.path.abspath(os.path.normpath(new_root))
        
        return FileList(link_items())        
        
    #%%-----------------------------------------------------------------------#  
    @check_other
    def maskedby(self, other, key='name', inverse=False):
        
        def get():
            
            for item, name in zip(self, names_self):
                
                if name in names_other:
                    
                    if inverse:
                        yield False                        
                    else:                        
                        yield True
                
                else:
                    
                    if inverse:                        
                        yield True                    
                    else:                        
                        yield False
                
        names_self = getattr(self, key + 's')()
            
        names_other = getattr(other, key + 's')()
        
        return list(get())
                 
#%%---------------------------------------------------------------------------#
class FileBase(FileList):
    
    name_indexfile = '~$indices.filebase'        
    name_filters = ['~$*']    
    threshold = 500
    
    #%%-----------------------------------------------------------------------#
    def __init__(self, *root, update=False, cache=False, threshold=None, nolink=True, use_exist=False):
                
        if not root:
            root = (os.getcwd(),)
            
        if cache and threshold is None:
            threshold = -1 
                    
        try:
            self.root, = root
            self.root = os.path.abspath(self.root)
                
            if not update and os.path.lexists(os.path.join(self.root, 
                                    FileBase.name_indexfile)):
    
                with open(os.path.join(self.root, 
                            FileBase.name_indexfile), 'r') as fobj:            
                    flist = (os.path.normpath(l.strip()) for l in fobj.readlines())
                    
                super().__init__(flist, root=self.root)
                    
            else:
                
                self.update(threshold=threshold, nolink=nolink, use_exist=use_exist)
                                            
        except ValueError:
            
            self.root = list(set(root))
            
            super().__init__(sum((FileBase(rt, update=update, threshold=threshold) for 
                                 rt in self.root), FileList([])))
                         
    #%%-----------------------------------------------------------------------#
    @staticmethod
    def list_files(root, *, start=None, nolink=True, use_exist=False):
        
        assert os.path.lexists(root)
                
        if start is None:
            
            start = root
            
        for root_, dirs, files in os.walk(root):
                        
            if not os.path.islink(root_):
                
                
                if use_exist and os.path.lexists(os.path.join(root_, FileBase.name_indexfile)):
                    
                    with open(os.path.join(root_, 
                            FileBase.name_indexfile), 'r') as fobj:            
                        files = (l.strip() for l in fobj.readlines())
                        
                    del dirs[:]
                    
                    relroot = os.path.relpath(root_, start)
                                        
                    yield from (os.path.normpath(os.path.join(relroot, f)) for f in files)
                
                else:
                    for f in files:
                                            
                        p = os.path.normpath(os.path.join(root_, f))
                        
                        if not os.path.islink(p) or not nolink:
                            
                            yield os.path.relpath(p, start)
                            
    #%%-----------------------------------------------------------------------#
    def update(self, threshold=None, nolink=True, use_exist=False):
        
        if isinstance(self.root, str):
            
            if threshold is None:
            
                threshold = FileBase.threshold 
            
            flist = set(FileBase.list_files(self.root, nolink=nolink, use_exist=use_exist))
            
            waste = set([])
            
            for flt in FileBase.name_filters:
                
                waste |= set(fnmatch.filter(flist, flt))
                
            flist = sorted(flist - waste)
            

            if len(flist) > threshold or os.path.isfile(
                                os.path.join(self.root, FileBase.name_indexfile)):
                try:
                    with open(os.path.join(self.root, 
                                        FileBase.name_indexfile), 'w') as fobj:
                        
                        fobj.write('\n'.join(flist))
                        
                except OSError:
                    pass
    
            super().__init__(flist, root=self.root)

        else:

            super().__init__(sum((FileBase(rt, update=True, 
                 threshold=threshold) for rt in self.root), FileList([])))
                
        return self
                            
#%%---------------------------------------------------------------------------#
    
if __name__ == '__main__':
    
    db = FileBase('../_run_151022', '../_run_160114', )
        
    lst1 = db['*.dyn']
    
    lst4 = lst1.copy().flatted()
        
    lst2 = (db['*.py'] < 1e6)
        
    lst3 = lst2.copy()
    
    lst3.extend(lst1)
    
    lst3.openwith(lambda x: open(x, 'r'))
    
    lst3 += lst1
    
    lst4 = FileBase('../_test')
    
    lst5 = FileBase('../_test1')
        
    seleted = (db.copy() < '1mb')['</'*3]
    
    print(seleted.tree())
    
   

    
    
    
    
    
    