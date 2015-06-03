import sys
IS_PYTHON_3K = 0

try:
    raw_input = raw_input
except:
    raw_input = input


try:
    if sys.version_info[0] == 3:
        IS_PYTHON_3K = 1
except:
    #That's OK, not all versions of python have sys.version_info
    pass

if IS_PYTHON_3K:
    def AsBytes(s):
        return s.encode('utf-8')

    def AsStr(s):
        if not isinstance(s, str):
            return s.decode('utf-8')
        return s

    def PushWriteBinary():
        sys.stdout = sys.__stdout__.buffer

    def PopWriteBinary():
        sys.stdout = sys.__stdout__

    def iteritems(d):
        return d.items()

    import builtins #@UnresolvedImport
    builtins.xrange = range
    builtins.raw_input = input
else:
    def AsBytes(s):
        return s

    def AsStr(s):
        return s

    def PushWriteBinary():
        pass

    def PopWriteBinary():
        pass

    def iteritems(d):
        return d.iteritems()