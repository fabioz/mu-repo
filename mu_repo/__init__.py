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

    if config_file is None: #Mostly for testing.
        contents = ''
    else:
        exists = os.path.exists(config_file)
        if not exists:
            contents = ''
        else:
            with open(config_file, 'r') as f:
                contents = f.read()

    config = Config.Create(contents)

    for arg in args:
        if arg.startswith('repo:'):
            args.remove(arg)
            config.repos = arg[len('repo:'):].replace(';', ',').split(',')
            if not args:
                Print('"repo" specified, but no additional args given.')
                return

        elif arg.startswith('repos:'):
            args.remove(arg)
            config.repos = arg[len('repos:'):].replace(';', ',').split(',')
            if not args:
                Print('"repos" specified, but no additional args given.')
                return

        elif arg == '--help':
            #On a help command, don't execute in multiple repos.
            config.repos = ['.']
            break

    else:
        if not config.repos:
            if '.' == args[0]:
                del args[0]
                config.repos.append('.')
            elif os.path.exists('.git'):
                #Allow it to be used on single git repos too.
                config.repos.append('.')


    arg0 = args[0]
    change_to_serial_if_possible = True
    update_repos_from_groups = True
    
    Run = None
    
    # actions related to repos or mu itself --------------------------------------------------------
    # This should be executed first, because some of them expect to see config as it was loaded
    if arg0 == 'set-var':
        from .action_set_var import Run #@Reimport
        change_to_serial_if_possible = False
        update_repos_from_groups = False

    elif arg0 == 'get-vars':
        from .action_get_vars import Run #@Reimport
        change_to_serial_if_possible = False

    elif arg0 == 'auto-update':
        from .action_auto_update import Run #@Reimport

    elif arg0 == 'list':
        from .action_list import Run #@Reimport

    elif arg0 == 'register':
        from .action_register import Run #@Reimport
        update_repos_from_groups = False
        
    elif arg0 == 'group':
        from .action_group import Run #@Reimport
        update_repos_from_groups = False

    # change global repos list to the current group, if any
    if update_repos_from_groups:
        group_repos = config.groups.get(config.current_group, None)
        if group_repos is not None:
            config.repos = group_repos 

    # acp variants ---------------------------------------------------------------------------------
    if arg0 == 'acp': #Add, commit, push
        def Run(params):
            from .action_add_commit_push import Run #@Reimport
            Run(params, add=True, commit=True, push=True)

    elif arg0 == 'ac': #Add, commit
        def Run(params):
            from .action_add_commit_push import Run #@Reimport
            Run(params, add=True, commit=True, push=False)

    elif arg0 == 'a': #Add
        def Run(params):
            from .action_add_commit_push import Run #@Reimport
            Run(params, add=True, commit=False, push=False)

    elif arg0 == 'c': #Commit
        def Run(params):
            from .action_add_commit_push import Run #@Reimport
            Run(params, add=False, commit=True, push=False)

    elif arg0 == 'p': #Push
        def Run(params):
            from .action_add_commit_push import Run #@Reimport
            Run(params, add=False, commit=False, push=True)




    # related to git actions -----------------------------------------------------------------------
    elif arg0 == 'dd':
        from .action_diff import Run #@Reimport

    elif arg0 == 'up':
        from .action_up import Run #@Reimport

    elif arg0 in ('sync', 'upd'):
        from .action_sync import Run #@Reimport

    elif arg0 == 'st': #Concise status message (branch, changes)
        from .action_st import Run #@Reimport

    elif arg0 == 'rb': #Rebase current_branch origin/current_branch
        from .action_rebase import Run #@Reimport


    # assorted -------------------------------------------------------------------------------------
    elif arg0 == 'install':
        from .action_install import Run #@Reimport

    elif arg0 == 'mu-patch':
        from .action_mu_patch import Run #@Reimport

    elif arg0 == 'post-review':
        from .action_post_review import Run #@Reimport

    elif arg0 == 'fix-eol':
        from .action_fix_eol import Run #@Reimport

    elif arg0 == 'github-request':
        from .action_github_pull_request import Run #@Reimport

    elif arg0 == 'howto':
        from .howto import Run #@Reimport

    elif arg0 == 'shell':
        import subprocess
        try:
            subprocess.call(['sh', '--login', '-i'])
        except:
            #Ignore any error here (if the user pressed Ctrl+C before exit, we'd have an exception).
            import traceback;traceback.print_exc()
        return


    # default action -------------------------------------------------------------------------------
    if Run is None:
        if arg0 == 'stash' and len(args) == 1:
            #Fixing stash: if git stash is provided without arguments, append a '-u' so that it
            #also stashes untracked files.
            args.append('-u')

        from .action_default import Run #@Reimport

    if change_to_serial_if_possible:
        if len(config.repos) == 1:
            config.serial = True

    return Run(Params(config, args, config_file))


if '--timeit' in sys.argv:
    sys.argv.remove('--timeit')
    main = PrintTime(main)



