import os.path
import sys
import subprocess
import threading

#===================================================================================================
# Status
#===================================================================================================
class Status(object):

    __slots__ = ['status_message', 'succeeded', 'config']

    def __init__(self, status_message, succeeded, config=None):
        self.status_message = status_message
        self.succeeded = succeeded
        self.config = config

def Indent(txt):
    return '\n'.join('  ' + line for line in  txt.splitlines()) + '\n'


#===================================================================================================
# ExecuteCommandThread
#===================================================================================================
class ExecuteCommandThread(threading.Thread):

    def __init__(self, repo, args):
        self.repo = repo
        self.args = args
        threading.Thread.__init__(self)
        self.stdout = ''
        self.stderr = ''

    def run(self):
        args = self.args
        repo = self.repo
        cmd = ['git'] + args
        self.stdout += ' '.join([repo, ':'] + cmd + ['\n'])
        p = subprocess.Popen(cmd, cwd=repo, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
        stdout, stderr = p.communicate()
        if stdout:
            self.stdout += Indent(stdout)
        if stderr:
            self.stderr += Indent(stderr)


#===================================================================================================
# main
#===================================================================================================
def main(config_file='.mu_repo', args=None, stream=None):
    if stream is None:
        stream = sys.stdout

    if args is None:
        args = sys.argv[1:]

    if len(args) == 0:
        msg = '''Mu is a command-line utility to deal with multiple git repositories.
        
It works with a .mu_repo file in the current working dir which provides the configuration
of the directories that should be tracked on commands.

To add a new repository to be tracked, one can do:

mu register repo1 repo2

mu list: lists the currently tracked repositories.

Any other command (such as the ones below) is passed directly to git through the multiple repositories:
 
mu pull
mu fetch
mu push
mu checkout release

'''
        print >> stream, msg
        return Status(msg, False)

    exists = os.path.exists(config_file)
    if not exists:
        contents = ''
    else:
        with open(config_file, 'r') as f:
            contents = f.read()
    config = ParseConfig(contents)

    if args[0] == 'register':
        if len(args) < 2:
            msg = 'Repository (dir name) to track not passed'
            print >> stream, msg
            return Status(msg, False)
        repos = config.repos
        msgs = []
        for repo in args[1:]:
            if repo in repos:
                msg = 'Repository: %s not added (already there)' % (repo,)
                print >> stream, msg
                msgs.append(msg)
            else:
                repos.append(repo)
                msg = 'Repository: %s added' % (repo,)
                print >> stream, msg
                msgs.append(msg)

        with open(config_file, 'w') as f:
            f.write(ConfigToString(config))

        return Status('\n'.join(msgs), True, config)

    elif args[0] == 'list':
        repo_str = '\n'.join(sorted(config.repos))
        print >> stream, 'Repositories:'
        print >> stream, repo_str
        return Status(repo_str, True, config)

    else:
        if not config.repos:
            msg = 'No repository registered. Use mu register repo_name to register repository.'
            print >> stream, msg
            return Status(msg, False, config)

        threads = []
        for repo in config.repos:
            if not os.path.exists(repo):
                print >> stream, '%s does not exist'
            else:
                t = ExecuteCommandThread(repo, args)
                t.start()
                threads.append(t)

        for t in threads:
            t.join()

        for t in threads:
            if t.stdout:
                print >> stream, t.stdout
            if t.stderr:
                print >> stream, t.stderr


    return Status('Finished', True)


#===================================================================================================
# ConfigToString
#===================================================================================================
def ConfigToString(config):
    lst = []
    for key, val in config.iteritems():
        if isinstance(val, list):
            assert key.endswith('s')
            key = key[:-1]
            for v in val:
                lst.append('%s=%s' % (key, v))
        else:
            raise AssertionError('Expecting val to be a list of strings.')

    return '\n'.join(lst)


#===================================================================================================
# Config
#===================================================================================================
class Config(object):

    __slots__ = ['repos']

    def __init__(self, **kwargs):
        self.repos = []
        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    def __getitem__(self, key):
        return getattr(self, key)

    def iteritems(self):
        yield ('repos', self.repos)

    def __eq__(self, o):
        if isinstance(o, Config):
            return self.repos == o.repos

        return False

    def __ne__(self, o):
        return not self == o

#===================================================================================================
# ParseConfig
#===================================================================================================
def ParseConfig(contents):
    lines = contents.splitlines()

    config = Config()

    for line in lines:
        line = line.strip()
        if line.startswith('repo'):
            l1 = line[4:].strip()
            if l1.startswith('='):
                l1 = l1[1:].strip()
                config.repos.append(l1)
    return config




