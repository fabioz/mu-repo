from mu_repo.action_diff import ExecuteGettingStdOutput, ParsePorcelain
import os.path

def Fix(root, filename):
    path = os.path.join(root, filename)
    contents = open(path, 'rb').read()
    if '\r' in contents:
        print 'Fixing:', path
        contents = contents.replace('\r\n', '\n').replace('\r', '\n')
        open(path, 'wb').write(contents)

def Run(params):
    config = params.config
    for repo in config.repos:
        stdout = ExecuteGettingStdOutput([config.git or 'git'] + 'status --porcelain -z'.split(), repo)
        for entry in ParsePorcelain(stdout):
            Fix(repo, entry.filename)
