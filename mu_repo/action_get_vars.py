'''
Created on 17/05/2012

@author: Fabio Zadrozny
'''
from mu_repo.print_ import Print
from mu_repo import Status

#===================================================================================================
# Run
#===================================================================================================
def Run(params):

    msg = str(params.config)
    Print(msg, file=params.stream)
    return Status(msg, True, params.config)
