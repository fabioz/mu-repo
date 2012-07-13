from mu_repo.action_diff import ParsePorcelain
import os.path
from mu_repo.execute_command import ExecuteGettingStdOutput
from mu_repo.print_ import Print

#===================================================================================================
# Fix
#===================================================================================================
def Fix(root, filename):
    path = os.path.join(root, filename)
    contents = open(path, 'rb').read()
    if '\r' in contents:
        Print('Fixing:', path)
        contents = contents.replace('\r\n', '\n').replace('\r', '\n')
        open(path, 'wb').write(contents)


#===================================================================================================
# Run
#===================================================================================================
def Run(params):
    config = params.config
    for repo in config.repos:
        stdout = ExecuteGettingStdOutput(
            [config.git or 'git'] + 'status --porcelain -z'.split(), repo)

        for entry in ParsePorcelain(stdout):
            Fix(repo, entry.filename)
