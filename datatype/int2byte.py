# -*- coding: utf-8 -*-

import re

#%%---------------------------------------------------------------------------#
class Int2Byte(int):
    
    '''
    covert integer number to readable byte format
    '''
    
    byte_pattern = re.compile(r'([0-9eE.]+)([ bkmgt]+)', re.I)
    
    decimals = 3
            
    factors = {'B': 1, 'KB': 1e3, 'MB': 1e6, 'GB': 1e9, 'TB': 1e12,
               'K': 1e3, 'M': 1e6, 'G': 1e9, 'T': 1e12}

    #%%-----------------------------------------------------------------------#        
    def __new__(cls, s, decimals=None):
        
        if isinstance(s, str):
            
            (value, unit), = Int2Byte.byte_pattern.findall(s.strip())
            
            s = float(value) * Int2Byte.factors[unit.strip().upper()]
        
        obj = super().__new__(cls, s)

        obj.decimals = Int2Byte.decimals if decimals is None else decimals

        obj.str = '{{:0.{}f}}'.format(int(obj.decimals))
        
        return obj
#%%---------------------------------------------------------------------------#