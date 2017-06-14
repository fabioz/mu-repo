'''
Created on 17/05/2012

@author: Fabio Zadrozny
'''
import sys

from mu_repo.backwards import iteritems


#===================================================================================================
# IsFalse
#===================================================================================================
def IsFalse(value):
    return value.strip().lower() in ('0', 'false', 'no')


#===================================================================================================
# IsTrue
#===================================================================================================
def IsTrue(value):
    return not IsFalse(value)



#===================================================================================================
# Config
#===================================================================================================
class Config(object):

    __slots__ = [
        'repos',
        'serial',
        '_git',
        'current_group',
        'groups',
        'is_sh_command',
        '_remote_hosts'
    ]

    def __init__(self, **kwargs):
        self.repos = []
        self.serial = False #Default is now in parallel.
        self._git = None
        self.is_sh_command = False

        # contains the current group; if None, all repos will be used
        self.current_group = None

        # groups of repositories, as a dict of { group_name : list of repo names }
        self.groups = {}
        for k, v in kwargs.items():
            setattr(self, k, v)

        self._remote_hosts = None

    def __getitem__(self, key):
        return getattr(self, key)

    def _GetGit(self):
        return self._git or 'git'

    def _SetGit(self, git):
        self._git = git

    git = property(_GetGit, _SetGit)

    def _GetRemoteHosts(self):
        remote_hosts = self._remote_hosts
        if remote_hosts is None:
            # Lazily-calculate (and then cache it).
            git = self.git
            from mu_repo.execute_command import ExecuteCommand
            output = ExecuteCommand(
                [git] + 'config --get-regexp mu-repo.remote-base-url'.split(), '.', return_stdout=True)

            remotes_hosts = []
            for line in output.splitlines():
                if line.startswith(b'mu-repo.remote-base-url '):
                    line = line[len(b'mu-repo.remote-base-url '):]
                    if type(b'') is not type(''):
                        line = line.decode('utf-8')
                    remotes_hosts.append(line)
            self._remote_hosts = remotes_hosts

        return self._remote_hosts

    def _SetRemoteHosts(self, remote_hosts):
        self._remote_hosts = remote_hosts[:]

    remote_hosts = property(_GetRemoteHosts, _SetRemoteHosts)


    def items(self):
        yield ('repos', self.repos)
        yield ('serial', str(self.serial))
        if self._git:
            yield ('git', self._git)
        if self.current_group:
            yield ('current_group', self.current_group)
        yield ('groups', self.groups)

        if self._remote_hosts:
            yield ('remote_hosts', self.remote_hosts)

    def __eq__(self, o):
        if isinstance(o, Config):
            return self.repos == o.repos and \
                self.current_group == o.current_group and \
                self.groups == o.groups

        return False

    def __ne__(self, o):
        return not self == o


    @classmethod
    def Create(cls, contents):
        lines = contents.splitlines()

        config = Config()

        def GetField(line):
            try:
                name, value = line.split('=')
            except:
                raise ValueError('Error when splitting line: %s at "="' % (line,))
            return name.strip(), value.strip()

        for line in lines:
            line = line.strip()
            if line:
                name, value = GetField(line)
                if name == 'repo':
                    config.repos.append(value)

                elif name == 'serial':
                    config.serial = IsTrue(value)

                elif name == 'git':
                    config._git = value

                elif name == 'remote_host':
                    if config._remote_hosts is None:
                        config._remote_hosts = []
                    config._remote_hosts.append(value)

                elif name == 'current_group' and value:
                    config.current_group = value

                elif name == 'group':
                    values = [x.strip() for x in value.split(',')]
                    if values:
                        group_name = values[0]
                        repos = values[1:]
                        config.groups[group_name] = repos

        return config

    def __str__(self):
        lst = []
        for key, val in self.items():
            if isinstance(val, str):
                lst.append('%s=%s' % (key, val))

            elif isinstance(val, list):
                assert key[-1] == 's'  # (change repos->repo or remote_hosts->remote_host)
                key = key[:-1]
                for v in sorted(val):
                    lst.append('%s=%s' % (key, v))

            elif isinstance(val, dict):
                assert key == 'groups'
                for group_name, repos in sorted(iteritems(val)):
                    values = [group_name] + repos
                    lst.append('group=%s' % ', '.join(values))
            else:
                raise AssertionError('Expecting val to be a list of strings.')

        return '\n'.join(lst)


    def __repr__(self):
        attrs = ['%s=%r' % (k, v) for (k, v) in self.items()]
        return 'Config(%s)' % ', '.join(attrs)

def UseShellOnSubprocess():
    return sys.platform == 'win32'
