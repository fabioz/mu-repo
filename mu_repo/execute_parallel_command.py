
#===================================================================================================
# ParallelCmd
#===================================================================================================
class ParallelCmd(object):

    __slots__ = ['cmd', 'repo']

    def __init__(self, repo, cmd):
        self.cmd = cmd
        self.repo = repo


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



