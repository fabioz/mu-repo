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
    try:
        msg = ' '.join(args)
    except:
        msg = ' '.join(str(x) for x in args)
    f.write(msg)
    f.write('\n')

