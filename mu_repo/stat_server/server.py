
_DEBUG = True

class _MutexHolder:
    system_mutex = None

class ServerAPI(object):

    def __init__(self, server):
        self.server = server
        self._shutdown = False

    def stat(self, git, repos):
        if _DEBUG:
            print('debug: stat', git, repos)

        from mu_repo.action_st import ExecuteStCommand
        from mu_repo import CreateParams

        def Print_(msg, repos):
            pass

        params = CreateParams(['st'])
        ExecuteStCommand(params, repos, git, Print_)

        return ''
    
    def kill(self):
        if _DEBUG:
            print('debug: Shutting down server')
        self._shutdown = True
        return ''
    
    def _serve_forever(self):
        while not self._shutdown:
            self.server.handle_request()

def start_server():
    from SimpleXMLRPCServer import SimpleXMLRPCServer
    import threading
    from mu_repo.system_mutex import SystemMutex

    system_mutex = SystemMutex('.mu_repo_stat_server_port')
    if system_mutex.get_mutex_aquired():
        # Make sure it's not garbage collected so that we hold the mutex
        _MutexHolder.system_mutex = system_mutex
        server = SimpleXMLRPCServer(("127.0.0.1", 0), logRequests=_DEBUG)
        host, port = server.socket.getsockname()
        system_mutex.write(str(port))
        if _DEBUG:
            print('debug: Started server at port: %s' % (port,))

        server_api = ServerAPI(server)
        server.register_instance(server_api)

        threading.Thread(target=server_api._serve_forever).start()
        return host, port
    else:
        if _DEBUG:
            with open(system_mutex.filename, 'r') as stream:
                port = stream.read().strip()
            print('debug: ServerAPI previously started at port: %s' % (port,))

def stop_server():
    from mu_repo.system_mutex import SystemMutex
    system_mutex = SystemMutex('.mu_repo_stat_server_port')
    if not system_mutex.get_mutex_aquired():
        with open(system_mutex.filename, 'r') as stream:
            port = stream.read().strip()

        import xmlrpclib
        s = xmlrpclib.ServerProxy('http://127.0.0.1:%s' % (port,))
        if _DEBUG:
            print('debug: Killing server')

        s.kill()

def start_in_subprocess():
    import os
    import sys
    import subprocess

    os.path
    env = os.environ.copy()
    env['PYTHONPATH'] = os.environ.get('PYTHONPATH', '') + os.pathsep + os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    subprocess.Popen([sys.executable, __file__], env=env)


if __name__ == '__main__':
    start_server()




