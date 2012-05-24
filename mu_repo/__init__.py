import os.path
import sys
from mu_repo.config import Config
from .print_ import Print

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
    #stream = params.stream
    #config_file = params.config_file
    #config = params.config

    __slots__ = ['config', 'args', 'config_file', 'stream']

    def __init__(self, config, args, config_file, stream):
        self.config = config
        self.args = args
        self.config_file = config_file
        self.stream = stream


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
def main(config_file='.mu_repo', args=None, stream=None):

    if args is None:
        args = sys.argv[1:]

    if len(args) == 0 or (len(args) == 1 and args[0] in ('help', '--help')):
        msg = '''mu-repo is a command-line utility to deal with multiple git repositories.
        
It works with a .mu_repo file in the current working dir which provides the 
configuration of the directories that should be tracked on commands.

* mu register repo1 repo2: registers repo1 and repo2 to be tracked.

* mu list: lists the currently tracked repositories.

* mu set-var git=d:/bin/git/bin/git.exe

* mu get-vars: prints the configuration file

* mu dd: creates a directory structure with working dir vs head and opens 
  WinMerge with it.

* mu . command: the config file is ignored, and mu works in the current dir, 
  not on registered subdirs (useful for "mu . dd" in a given git repository)

Any other command is passed directly to git through the multiple repositories:
I.e.:

mu pull
mu fetch
mu push
mu checkout release

Also, it defines some shortcuts:

mu st         = git status --porcelain
mu co branch  = git checkout branch
mu mu-patch   = git diff --cached --full-index > pasting output to file for each repo 
mu mu-branch  = git rev-parse --abbrev-ref HEAD

Note: Passing --timeit in any command will print the time it took
      to execute the command.
'''
        Print(msg, file=stream)
        return Status(msg, False)

    exists = os.path.exists(config_file)
    if not exists:
        contents = ''
        if '.' == args[0]:
            del args[0]
            contents = 'repo=.'
    else:
        with open(config_file, 'r') as f:
            contents = f.read()
    config = Config.Create(contents)

    arg0 = args[0]
    if arg0 == 'set-var':
        from .action_set_var import Run

    elif arg0 == 'get-vars':
        from .action_get_vars import Run #@Reimport

    elif arg0 == 'register':
        from .action_register import Run #@Reimport

    elif arg0 == 'dd':
        from .action_diff import Run #@Reimport

    elif arg0 == 'list':
        from .action_list import Run #@Reimport

    else:
        from .action_default import Run #@Reimport

    return Run(Params(config, args, config_file, stream))


if '--timeit' in sys.argv:
    sys.argv.remove('--timeit')
    main = PrintTime(main)



