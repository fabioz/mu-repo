'''
Created on 27/05/2012

@author: Fabio Zadrozny
'''
from mu_repo.print_ import Print

#===================================================================================================
# Run
#===================================================================================================
def Run(params):
    args = params.args[1:]
    if not args:
        Print('Message for commit is required for git add -A & git commit -m command.')
        return

    from .action_default import Run #@Reimport
    from mu_repo import Params
    Run(Params(params.config, ['add', '-A'], params.config_file, params.stream))
    Run(Params(params.config, ['commit', '-m', ' '.join(args)], params.config_file, params.stream))

