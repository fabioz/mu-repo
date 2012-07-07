from __future__ import with_statement
from . import backwards
import os.path
import sys
from mu_repo.config import Config
from .print_ import Print

#Just making sure we're in the PYTHONPATH!
sys.path.append(os.path.dirname(__file__))

#===================================================================================================
# Status
#===================================================================================================
class Status(object):

    __slots__ = ['status_message', 'succeeded', 'config']

    def __init__(self, status_message, succeeded, config=None):
        self.status_message = status_message
        self.succeeded = succeeded
        self.config = config

#===================================================================================================
# Params
#===================================================================================================
class Params(object):

    #args = params.args
    #config_file = params.config_file
    #config = params.config

    __slots__ = ['config', 'args', 'config_file']

    def __init__(self, config, args, config_file):
        self.config = config
        self.args = args
        self.config_file = config_file


#===================================================================================================
# PrintTime
#===================================================================================================
def PrintTime(func):
    import time
    def Exec(*args, **kwargs):
        curr_time = time.time()
        ret = func(*args, **kwargs)
        diff = time.time() - curr_time
        Print('Total time: %.2f' % (diff,))
        return ret
    return Exec


#===================================================================================================
# main
#===================================================================================================
def main(config_file='.mu_repo', args=None):
    '''
    Entry point.
    '''

    if args is None:
        args = sys.argv[1:]

    if len(args) == 0 or (len(args) == 1 and args[0] in ('help', '--help')):
        from string import Template
        from . import __docs__
        msg = __docs__.__doc__ #@UndefinedVariable
        Print(msg)
        return Status(msg, False)

    exists = os.path.exists(config_file)
    if not exists:
        contents = ''
    else:
        with open(config_file, 'r') as f:
            contents = f.read()
    config = Config.Create(contents)

    if not config.repos:
        if '.' == args[0]:
            del args[0]
            config.repos.append('.')
        elif os.path.exists('.git'):
            #Allow it to be used on single git repos too.
            config.repos.append('.')


    arg0 = args[0]
    change_to_serial_if_possible = True
    if arg0 == 'set-var':
        from .action_set_var import Run
        change_to_serial_if_possible = False

    elif arg0 == 'get-vars':
        from .action_get_vars import Run #@Reimport
        change_to_serial_if_possible = False

    elif arg0 == 'github-request':
        from .action_github_pull_request import Run #@Reimport

    elif arg0 == 'register':
        from .action_register import Run #@Reimport

    elif arg0 == 'fix-eol':
        from .action_fix_eol import Run #@Reimport

    elif arg0 == 'auto-update':
        from .action_auto_update import Run #@Reimport

    elif arg0 == 'list':
        from .action_list import Run #@Reimport

    elif arg0 == 'dd':
        from .action_diff import Run #@Reimport

    elif arg0 == 'up':
        from .action_up import Run #@Reimport

    elif arg0 in ('sync', 'upd'):
        from .action_sync import Run #@Reimport

    elif arg0 == 'a': #Add
        def Run(params):
            from .action_add_commit_push import Run #@Reimport
            Run(params, add=True, commit=False, push=False)

    elif arg0 == 'ac': #Add, commit
        def Run(params):
            from .action_add_commit_push import Run #@Reimport
            Run(params, add=True, commit=True, push=False)

    elif arg0 == 'acp': #Add, commit, push
        def Run(params):
            from .action_add_commit_push import Run #@Reimport
            Run(params, add=True, commit=True, push=True)

    elif arg0 == 'p': #Push
        def Run(params):
            from .action_add_commit_push import Run #@Reimport
            Run(params, add=False, commit=False, push=True)

    elif arg0 == 'st': #Concise status message (branch, changes)
        from .action_st import Run #@Reimport


    elif arg0 == 'shell':
        import subprocess
        try:
            subprocess.call(['sh', '--login', '-i'])
        except:
            #Ignore any error here (if the user pressed Ctrl+C before exit, we'd have an exception).
            import traceback;traceback.print_exc()
        return

    else:
        from .action_default import Run #@Reimport

    if change_to_serial_if_possible:
        if len(config.repos) == 1:
            config.serial = True

    return Run(Params(config, args, config_file))


if '--timeit' in sys.argv:
    sys.argv.remove('--timeit')
    main = PrintTime(main)



