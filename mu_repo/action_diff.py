'''
Created on 19/05/2012

@author: Fabio Zadrozny
'''
from mu_repo import thread_pool
from mu_repo.print_ import Print
import os.path
import shutil
import subprocess

#===================================================================================================
# ExecuteGettingStdOutput
#===================================================================================================
def ExecuteGettingStdOutput(cmd, cwd):
    p = subprocess.Popen(
        cmd,
        cwd=cwd,
        stderr=subprocess.STDOUT,
        stdout=subprocess.PIPE,
        stdin=subprocess.PIPE
    )

    stdout, _stderr = p.communicate()
    return stdout



#===================================================================================================
# CreateFromGit
#===================================================================================================
class CreateFromGit(object):

    def __init__(self, *args):
        self._args = args

    def __call__(self):
        join, temp_repo, repo, changed_file_fullpath = self._args
        stdout = ExecuteGettingStdOutput(
            'git show HEAD:%s' % (changed_file_fullpath,), repo)
        with open(join(temp_repo, repo, changed_file_fullpath), 'wb') as f:
            f.write(stdout)


#===================================================================================================
# Run
#===================================================================================================
def Run(params):
    config = params.config
    git = config.git or 'git'

    dirname = os.path.dirname
    join = os.path.join

    temp_dir_name = '.mu.diff.git.tmp'

    if os.path.exists(temp_dir_name):
        n = ''
        while n not in ('y', 'n'):
            n = raw_input(
                'Temporary dir for diff: %s already exists. Delete and continue (Y/n) or cancel (N/n)?' %
                (temp_dir_name,)
            ).strip().lower()
            if n == 'y':
                shutil.rmtree(temp_dir_name)
                break
            if n == 'n':
                Print('Canceling diff action.')
                return

    temp_working = join(temp_dir_name, 'WORKING')
    temp_repo = join(temp_dir_name, 'REPO')
    os.mkdir(temp_dir_name)
    os.mkdir(temp_working)
    os.mkdir(temp_repo)

    #===============================================================================================
    # Define symlink utility
    #===============================================================================================
    keep_files_synched = None
    try:
        if not hasattr(os, 'symlink'):
            import win32file
            #Note: not all users can do it...
            #http://stackoverflow.com/questions/2094663/determine-if-windows-process-has-privilege-to-create-symbolic-link
            #see: http://bugs.python.org/issue1578269
            #see: http://technet.microsoft.com/en-us/library/cc766301%28WS.10%29.aspx
            def symlink(src, target):
                win32file.CreateSymbolicLink(src, target, 1)
        else:
            symlink = os.symlink

        #Just check if it does indeed work... if it doesn't redefine and use our polling strategy.
        symlink(temp_working, join(temp_dir_name, 'lnk_test'))
    except:
        from mu_repo import keep_files_synched
        def symlink(src, target):
            shutil.copyfile(src, target)
            keep_files_synched.KeepInSync(src, target)

    try:
        #Note: we could use diff status --porcelain instead if we wanted to check untracked files.
        cmd = [git] + 'diff HEAD --name-only -z'.split()
        for repo in config.repos:
            stdout = ExecuteGettingStdOutput(cmd, repo)
            for changed_file_fullpath in stdout.split('\0'):
                if changed_file_fullpath:
                    fdir = dirname(changed_file_fullpath)

                    if not os.path.exists(join(temp_working, repo, fdir)):
                        os.makedirs(join(temp_working, repo, fdir))
                    symlink(
                        join(repo, changed_file_fullpath),
                        join(temp_working, repo, changed_file_fullpath)
                    )

                    temp_repo_dir = join(temp_repo, repo, fdir)
                    if not os.path.exists(temp_repo_dir):
                        os.makedirs(temp_repo_dir)

                    thread_pool.AddTask(
                        CreateFromGit(join, temp_repo, repo, changed_file_fullpath))
        thread_pool.Join()

        winmerge_cmd = 'WinMergeU.exe /r /u /wr /dl WORKINGCOPY /dr HEAD'.split()
        cmd = winmerge_cmd + [temp_working, temp_repo]
        try:
            subprocess.call(cmd)
        except:
            Print('Error calling: %s' % (' '.join(cmd),))

        #If we've gono to the synching mode, make sure we had a last synchronization before
        #getting out of the diff.
        if keep_files_synched is not None:
            keep_files_synched.StopSyncs()
    finally:
        def onerror(*args):
            Print('Error removing temporary directory structure: %s' % (args,))
        shutil.rmtree(temp_dir_name, onerror=onerror)





