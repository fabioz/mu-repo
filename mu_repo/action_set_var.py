'''
Created on 17/05/2012

@author: Fabio Zadrozny
'''
from __future__ import with_statement
from mu_repo.config import IsFalse
from mu_repo import Status
from mu_repo.print_ import Print


#===================================================================================================
# Run
#===================================================================================================
def Run(params):
    args = params.args
    if len(args) != 2 or args[1].count('=') != 1:
        msg = 'Syntax for set-var is "mu set-var key=value"'
        Print(msg)
        return Status(msg, True, params.config)

    var, value = args[1].split('=')
    var = var.strip().lower()
    if var == 'serial':
        if IsFalse(value):
            params.config.serial = False
        else:
            params.config.serial = True

    elif var == 'git':
        params.config.git = value

    else:
        msg = 'Variable to set: "%s" not recognized.' % (var,)
        Print(msg)
        return Status(msg, False, params.config)

    with open(params.config_file, 'w') as f:
        f.write(str(params.config))

    msg = 'Variable %s set to %s' % (var, value)
    Print(msg)
    return Status(msg, True, params.config)



