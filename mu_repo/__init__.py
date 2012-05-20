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
#@PrintTime # -uncomment to see times.
def main(config_file='.mu_repo', args=None, stream=None):

    if args is None:
        args = sys.argv[1:]

    if len(args) == 0:
        msg = '''Mu is a command-line utility to deal with multiple git repositories.
        
It works with a .mu_repo file in the current working dir which provides the configuration
of the directories that should be tracked on commands.

To add a new repository to be tracked, one can do:

mu register repo1 repo2

mu list: lists the currently tracked repositories.

mu set_var git=d:/bin/git/bin/git.exe

mu get_vars

Any other command (such as the ones below) is passed directly to git through the multiple repositories:
 
mu pull
mu fetch
mu push
mu checkout release

'''
        Print(msg, file=stream)
        return Status(msg, False)

    exists = os.path.exists(config_file)
    if not exists:
        contents = ''
    else:
        with open(config_file, 'r') as f:
            contents = f.read()
    config = Config.Create(contents)

    if args[0] == 'set_var':
        from .action_set_var import Run

    elif args[0] == 'get_vars':
        from .action_get_vars import Run #@Reimport

    elif args[0] == 'register':
        from .action_register import Run #@Reimport

    elif args[0] == 'dd':
        from .action_diff import Run #@Reimport

    elif args[0] == 'list':
        from .action_list import Run #@Reimport

    else:
        from .action_default import Run #@Reimport

    return Run(Params(config, args, config_file, stream))





