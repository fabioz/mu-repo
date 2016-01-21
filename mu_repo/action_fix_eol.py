from mu_repo.action_diff import ParsePorcelain
import os.path
from mu_repo.execute_command import ExecuteGettingStdOutput
from mu_repo.print_ import Print
import sys

#===================================================================================================
# Fix
#===================================================================================================
def Fix(root, filename):
    path = os.path.join(root, filename)
    if not os.path.exists(path):
        Print('Skip removed file:', path)
        return
    
    contents = open(path, 'rb').read()
    if b'\r' in contents:
        Print('Fixing:', path)
        contents = contents.replace(b'\r\n', b'\n').replace(b'\r', b'\n')
        open(path, 'wb').write(contents)


#===================================================================================================
# Run
#===================================================================================================
def Run(params):
    config = params.config
    for repo in config.repos:
        stdout = ExecuteGettingStdOutput(
            [config.git or 'git'] + 'status --porcelain -z'.split(), repo)

        if sys.version_info[0] >= 3:
            stdout = stdout.decode(sys.getfilesystemencoding())
        for entry in ParsePorcelain(stdout):
            Fix(repo, entry.filename)
