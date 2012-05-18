'''
Created on 17/05/2012

@author: Fabio Zadrozny
'''
import sys

#===================================================================================================
# Print
#===================================================================================================
def Print(*args, **kwargs):
    f = kwargs.get('file')
    if f is None:
        f = sys.stdout
    f.write(' '.join(args))
    f.write('\n')

