'''
Created on 17/05/2012

@author: Fabio Zadrozny
'''
from mu_repo.backwards import AsBytes, PopWriteBinary, PushWriteBinary, iteritems
import sys

START_COLOR = '${START_COLOR}'
RESET_COLOR = '${RESET_COLOR}'



try:
    def _InitWin32():

        from mu_repo import _color_console
        _color_console

        #===========================================================================================
        # Console
        #===========================================================================================
        class _Console(object):

            def __init__(self):
                colors = dict(
                    BLACK=[],
                    BLUE=['BLUE'],
                    CYAN=['GREEN', 'BLUE'],
                    GREEN=['GREEN'],
                    MAGENTA=['RED', 'BLUE'],
                    RED=['RED'],
                    WHITE=['RED', 'GREEN', 'BLUE'],
                    YELLOW=['RED', 'GREEN'],
                )


                self._foreground_map = color_map = { '' : 0 }
                for color_name, color_components in iteritems(colors):
                    if color_components:
                        value = _color_console.FOREGROUND_INTENSITY
                    else:
                        value = 0
                    for component in color_components:
                        value |= getattr(_color_console, 'FOREGROUND_' + component)
                    color_map[color_name] = value

                #Some of the calls below could raise exceptions, in which case we should
                #fallback to another approach!
                self._reset = _color_console.get_text_attr()

            def SetColor(self, foreground_color):
                _color_console.set_text_attr(self._foreground_map[foreground_color])

            def Reset(self):
                _color_console.set_text_attr(self._reset)

        return _Console()

    console = _InitWin32()


except:
    #If anything fails there, use the version that prints ascii chars.

    #===============================================================================================
    # Console
    #===============================================================================================
    class _Console(object):

        color_map = {
            'BLACK'   : 30,
            'BLUE'    : 34,
            'CYAN'    : 36,
            'GREEN'   : 32,
            'MAGENTA' : 35,
            'RED'     : 31,
            'WHITE'   : 37,
            'YELLOW'  : 33,
        }

        def _Escape(self, code):
            PushWriteBinary()
            try:
                sys.stdout.write(AsBytes('\033[') + code)
            finally:
                PopWriteBinary()

        def SetColor(self, foreground_color):
            self._Escape(AsBytes('%dm' % self.color_map[foreground_color]))

        def Reset(self):
            self._Escape(AsBytes('0m'))


    console = _Console()


_ignore_print = 0


#===================================================================================================
# PushIgnorePrint
#===================================================================================================
def PushIgnorePrint():
    global _ignore_print
    _ignore_print += 1


#===================================================================================================
# PopIgnorePrint
#===================================================================================================
def PopIgnorePrint():
    global _ignore_print
    _ignore_print -= 1


def PrintError(msg=''):
    from mu_repo.backwards_stringio import StringIO
    s = StringIO()
    s.write('\n===================================== ERROR =====================================\n')
    if msg:
        s.write(msg)
        s.write('\n\n')
    import traceback;traceback.print_exc(file=s)
    s.write('\n=================================================================================\n\n')

    #On a single write, the GIL should be locked, so, the output should still appear to be synched
    #for a single error.
    sys.stdout.write(s.getvalue())


#===================================================================================================
# Print
#===================================================================================================
def Print(*args, **kwargs):
    if _ignore_print:
        return

    color = kwargs.pop('__color__', 'CYAN')  # Default for ${START_COLOR} is CYAN

    assert 'file' not in kwargs
    f = sys.stdout
    try:
        msg = ' '.join(args)
    except:
        msg = ' '.join(str(x) for x in args)

    i = msg.find(START_COLOR)
    while i >= 0:
        write_without_color = msg[:i]
        f.write(write_without_color)

        msg = msg[i + len(START_COLOR):]
        i = msg.find(RESET_COLOR)
        if i >= 0:
            write_in_colors = msg[:i]
            msg = msg[i + len(RESET_COLOR):]
        else:
            write_in_colors = msg
            msg = '' #No RESET after start: go until end of string.

        console.SetColor(color)
        try:
            f.write(write_in_colors)
        finally:
            console.Reset()
        i = msg.find(START_COLOR)

    f.write(msg + '\n')


#===================================================================================================
# CreateJoinedReposMsg
#===================================================================================================
def CreateJoinedReposMsg(msg, repos):
    if msg.endswith(':'):
        msg += ' '
    if msg:
        msg = '${START_COLOR}%s${RESET_COLOR}' % (msg,)
    #'${START_COLOR}%s${RESET_COLOR}' % '${RESET_COLOR}, ${START_COLOR}'.join(sorted(repos))
    msg += ', '.join(sorted(repos))
    return msg

