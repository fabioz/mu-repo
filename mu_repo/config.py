'''
Created on 17/05/2012

@author: Fabio Zadrozny
'''

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
        'git',
    ]

    def __init__(self, **kwargs):
        self.repos = []
        self.serial = False
        self.git = None
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __getitem__(self, key):
        return getattr(self, key)

    def items(self):
        yield ('repos', self.repos)
        yield ('serial', str(self.serial))
        if self.git:
            yield ('git', self.git)

    def __eq__(self, o):
        if isinstance(o, Config):
            return self.repos == o.repos

        return False

    def __ne__(self, o):
        return not self == o


    @classmethod
    def Create(cls, contents):
        lines = contents.splitlines()

        config = Config()

        for line in lines:
            line = line.strip()
            if line:
                if line.startswith('repo'):
                    l1 = line[4:].strip()
                    if l1.startswith('='):
                        l1 = l1[1:].strip()
                        config.repos.append(l1)

                elif line.startswith('serial'):
                    l1 = line[6:].strip()
                    if l1.startswith('='):
                        l1 = l1[1:]
                        config.serial = IsTrue(l1)

                elif line.startswith('git'):
                    l1 = line[3:].strip()
                    if l1.startswith('='):
                        l1 = l1[1:]
                        config.git = l1.strip()

        return config

    def __str__(self):
        lst = []
        for key, val in self.items():
            if isinstance(val, str):
                lst.append('%s=%s' % (key, val))

            elif isinstance(val, list):
                assert key.endswith('s')
                key = key[:-1]
                for v in val:
                    lst.append('%s=%s' % (key, v))
            else:
                raise AssertionError('Expecting val to be a list of strings.')

        return '\n'.join(lst)
