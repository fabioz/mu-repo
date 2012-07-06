from mu_repo.print_ import START_COLOR, RESET_COLOR, Print
import subprocess

#===================================================================================================
# ExecuteCommand
#===================================================================================================
def ExecuteCommand(cmd, repo, communicate=False):
    msg = ' '.join([START_COLOR, '\n', repo, ':'] + cmd + [RESET_COLOR])
    Print(msg)
    try:
        if communicate:
            p = subprocess.Popen(cmd, cwd=repo, stdout=subprocess.PIPE)
        else:
            p = subprocess.Popen(cmd, cwd=repo)
    except:
        from mu_repo.print_ import PrintError
        PrintError('Error executing: ' + ' '.join(cmd) + ' on: ' + repo)
        raise

    if not communicate:
        p.wait()
    else:
        stdout, stderr = p.communicate()
        return stdout, stderr

