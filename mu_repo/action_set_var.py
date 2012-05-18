'''
Created on 17/05/2012

@author: Fabio Zadrozny
'''
from mu_repo.config import IsFalse
from mu_repo import Status
from mu_repo.print_ import Print


#===================================================================================================
# Run
#===================================================================================================
def Run(params):
    var, value = params.args[1].split('=')
    var = var.strip().lower()
    value = value.strip().lower()
    if var == 'serial':
        if IsFalse(value):
            params.config.serial = False
        else:
            params.config.serial = True
    else:
        return Status('Variable to set: %s not recognized.' % (var,), False, params.config)

    with open(params.config_file, 'w') as f:
        f.write(str(params.config))

    msg = 'Variable %s set to %s' % (var, value)
    Print(msg, file=params.stream)
    return Status(msg, True, params.config)



