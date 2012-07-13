from mu_repo.print_ import START_COLOR, RESET_COLOR, Print, PrintError
import subprocess

#===================================================================================================
# ExecuteCommand
#===================================================================================================
def ExecuteCommand(cmd, repo, return_stdout=False, verbose=True):
    '''
    Execute command letting stderr go to the default sys.stderr.
    Will block until the command finishes.
    
    @param cmd: list(str)
        The command to be executed.
        
    @param repo: str
        The repository (working dir) where the command should be executed.
    
    @param return_stdout: bool
        If True, will grab stdout and return it, otherwise will let it go to sys.stderr.
        
    @param verbose: bool
        If True will print the command being executed.
        
    @return: the redirected stdout (if return_stdout is True) or None otherwise
    '''
    if verbose:
        msg = ' '.join([START_COLOR, '\n', repo, ':'] + cmd + [RESET_COLOR])
        Print(msg)
    try:
        if return_stdout:
            p = subprocess.Popen(cmd, cwd=repo, stdout=subprocess.PIPE)
        else:
            p = subprocess.Popen(cmd, cwd=repo)
    except:
        PrintError('Error executing: ' + ' '.join(cmd) + ' on: ' + repo)
        raise

    if not return_stdout:
        p.wait()
    else:
        stdout, _stderr = p.communicate()
        return stdout



#===================================================================================================
# ExecuteGettingStdOutput
#===================================================================================================
def ExecuteGettingStdOutput(cmd, cwd):
    return ExecuteCommand(cmd, cwd, return_stdout=True, verbose=False)
