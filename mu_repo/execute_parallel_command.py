
#===================================================================================================
# ParallelCmd
#===================================================================================================
class ParallelCmd(object):

    __slots__ = ['cmd', 'repo']

    def __init__(self, repo, cmd):
        self.cmd = cmd
        self.repo = repo


#===================================================================================================
# ExecuteInParallelStackingMessages
#===================================================================================================
def ExecuteInParallelStackingMessages(commands, match_empty_output, execute_on_repos, serial=False):
    '''
    @param match_empty_output: callable
        Either the message we were expecting or a callable that returns True to mean this was
        the expected message or False otherwise.
        
    @param execute_on_repos: callable(str)
        A callable that receives the repositories that were matched as being empty.
        Not called if no repositories were matched.
    
    @return: list(str)
        Returns a list with the repositories that matched the expected output as empty.
        
    @see ExecuteInParallel for other commands.
    '''
    from .print_ import Print
    repos = []

    def on_output(output):
        if match_empty_output(output):
            repos.append(output.repo)
            return

        # Print message by default.
        Print(output)

    ExecuteInParallel(commands, on_output=on_output, serial=serial)
    if repos:
        execute_on_repos(repos)

    return repos


#===================================================================================================
# ExecuteInParallel
#===================================================================================================
def ExecuteInParallel(commands, on_output=None, serial=False):
    '''
    @param commands: list(ParallelCmd)
        The commands to execute.
        
    @param on_output: callable
        Method to be called when the command finishes and gives it output 
        (by default Prints the output).
        
    @param serial: bool
        This probably should not be here, but leave it for now: execute things in parallel instead.
    '''

    from mu_repo.execute_git_command_in_thread import ExecuteGitCommandThread
    try:
        import Queue
    except ImportError:
        import queue as Queue

    threads = []
    output_queue = Queue.Queue()
    for cmd in commands:
        t = ExecuteGitCommandThread(
            cmd.repo, cmd.cmd, output_queue)
        threads.append(t)

    if serial:
        for t in threads:
            t.run(serial=True) #When serial will print as is executing.
    else:
        from mu_repo.execute_git_command_in_thread import ExecuteThreadsHandlingOutputQueue
        ExecuteThreadsHandlingOutputQueue(threads, output_queue, on_output=on_output)



