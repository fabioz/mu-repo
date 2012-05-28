import os.path
import sys
from mu_repo.config import Config
from .print_ import Print

try:
    #Reference: http://stackoverflow.com/questions/287871/print-in-terminal-with-colors-using-python
    #To properly support colors, one has to enable http://support.microsoft.com/kb/101875
    #Or colorama must be used (it's currently distributed along with this project)
    #Gotten from http://pypi.python.org/pypi/colorama
    #See COLORAMA_LICENSE for details and copyright.
    import colorama
except:
    COLOR = ''
    RESET = ''
else:
    colorama.init()
    COLOR = colorama.Fore.CYAN
    RESET = colorama.Fore.RESET


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
        from string import Template
        msg = Template('''mu-repo is a command-line utility to deal with multiple git repositories.
        
It works with a .mu_repo file in the current working dir which provides the 
configuration of the directories that should be tracked on commands.

* ${START}mu register repo1 repo2:${END} Registers repo1 and repo2 to be tracked.
* ${START}mu register --all:${END} Marks for all subdirs with .git to be tracked.
* ${START}mu list:${END} Lists the currently tracked repositories.
* ${START}mu set-var git=d:/bin/git/bin/git.exe:${END} Set git location to be used.
* ${START}mu get-vars:${END} Prints the configuration file

* ${START}mu dd:${END}
     Creates a directory structure with working dir vs head and opens 
     WinMerge with it (doing mu ac will commit exactly what's compared in this
     situation)
     
     Also accepts a parameter to compare with a different commit/branch. I.e.:
     mu dd HEAD^^
     mu dd 9fd88da
     mu dd development

* ${START}mu . command: ${END} 
     The config file is ignored, and mu works in the current dir, 
     not on registered subdirs (useful for "mu . dd" in a given git repository)

Also, it defines some shortcuts:

${START}mu st         ${END}= git status --porcelain
${START}mu co branch  ${END}= git checkout branch
${START}mu mu-patch   ${END}= git diff --cached --full-index > output to file for each repo 
${START}mu mu-branch  ${END}= git rev-parse --abbrev-ref HEAD (print current branch)
${START}mu ac msg     ${END}= git add -A & git commit -m (the message must always be passed) 
${START}mu shell      ${END}= On msysgit, call sh --login -i (linux-like env)

Any other command is passed directly to git for each repository:
I.e.:

${START}mu pull            ${END}
${START}mu fetch           ${END}
${START}mu push            ${END}
${START}mu checkout release${END}

Note: Passing --timeit in any command will print the time it took
      to execute the command.
''').substitute(START=COLOR, END=RESET)
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

    elif arg0 == 'ac':
        from .action_add_and_commit import Run #@Reimport

    elif arg0 == 'shell':
        import subprocess
        try:
            subprocess.call(['sh', '--login', '-i'])
        except:
            #Ignore any error here (if the user pressed Ctrl+C before exit, we'd have an exception).
            pass
        return

    else:
        from .action_default import Run #@Reimport

    return Run(Params(config, args, config_file, stream))


if '--timeit' in sys.argv:
    sys.argv.remove('--timeit')
    main = PrintTime(main)



