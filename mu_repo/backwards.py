import sys
IS_PYTHON_3K = 0

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
        return s.decode('utf-8')

    def PushWriteBinary():
        sys.stdout = sys.__stdout__.buffer

    def PopWriteBinary():
        sys.stdout = sys.__stdout__

    import builtins
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
