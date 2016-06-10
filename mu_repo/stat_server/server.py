
_DEBUG = False


class _MutexHolder:
    system_mutex = None

def listen_changes_on_dir(directory, on_change_found):
    try:
        # A little sample on how it works...
        from mu_repo.stat_server.winapi import read_events, get_directory_handle
        try:
            handle = get_directory_handle(directory)
            while True:
                for _ev in read_events(handle, recursive=True):
                    if _ev.src_path not in ('.git\\index.lock', '.git'):
                        # Ignore changes in the index.lock (it's used even for status).
                        on_change_found()
        except WindowsError:
            pass  # Directory not there
    except ImportError:
        pass  # ctypes.wintypes not there


class ServerAPI(object):

    def __init__(self, server):
        self.server = server
        self._repos_to_branch_and_messages = {}
        self._listening_repos = set()
    
    def _listen_dir_to_invalidate_cache(self, repo):
        if repo not in self._listening_repos:
            self._listening_repos.add(repo)
            def on_change_found():
                if _DEBUG:
                    print('Invalidating cache for repo: %s' % (repo,))
                self._repos_to_branch_and_messages.pop(repo, None)

            import threading
            t = threading.Thread(target=listen_changes_on_dir, args=(repo, on_change_found))
            t.setDaemon(True)
            t.start()

    def stat(self, git, repos):
        if _DEBUG:
            print('debug: stat', git, repos)

        from mu_repo import CreateParams

        base_repos_to_branch_and_messages = {}
        missing_repos = []
        for repo in repos:
            branch_and_msg = self._repos_to_branch_and_messages.get(repo)
            if branch_and_msg is not None:
                if _DEBUG:
                    print('debug: Found cached for repo: %s' % (repo,))
                base_repos_to_branch_and_messages[repo] = branch_and_msg
            else:
                if _DEBUG:
                    print('debug: Cache missing for repo: %s' % (repo,))
                missing_repos.append(repo)

        params = CreateParams(['st'])
        if not params.config.repos:
            params.config.repos = ['.']

        from mu_repo.action_st import CollectStCacheOnRepos, CreateMessagesFromReposToBranchAndMessages
        if missing_repos:
            new_repos_to_branch_and_messages = CollectStCacheOnRepos(params, missing_repos, git)
            self._repos_to_branch_and_messages.update(new_repos_to_branch_and_messages)
            base_repos_to_branch_and_messages.update(new_repos_to_branch_and_messages)
            for repo in repos:
                self._listen_dir_to_invalidate_cache(repo)

        messages = CreateMessagesFromReposToBranchAndMessages(repos, base_repos_to_branch_and_messages)
        return messages
    
    def shutdown(self):
        if _DEBUG:
            print('debug: server: Shutting down server')
        self.server.shutdown()
        return ''
    

def start_server():
    from mu_repo.system_mutex import create_system_mutex_for_current_dir

    system_mutex = create_system_mutex_for_current_dir()
    if system_mutex.get_mutex_aquired():
        # Make sure it's not garbage collected so that we hold the mutex
        _MutexHolder.system_mutex = system_mutex

        #===========================================================================================
        # Start the server now that we have the mutex
        #===========================================================================================
        from mu_repo.umsgpack_s_conn import ConnectionHandler, UMsgPacker, Server

        class ServerHandler(ConnectionHandler, UMsgPacker):

            def _handle_decoded(self, decoded):
                try:
                    # Some message was received from the client in the server.
                    if decoded == 'echo':
                        # Actual implementations may want to put that in a queue and have an additional
                        # thread to check the queue and handle what was received and send the results back.
                        self.send('echo back')
                        return

                    elif decoded == 'shutdown':
                        # Actual implementations may want to put that in a queue and have an additional
                        # thread to check the queue and handle what was received and send the results back.
                        server_api.shutdown()
                        return

                    elif isinstance(decoded, (tuple, list)):
                        if len(decoded) == 3 and decoded[0] == 'stat':
                            self.send(server_api.stat(decoded[1], decoded[2]))
                            return

                    self.send('Error: %s did not match anything expected.' % (decoded,))
                except:
                    import traceback
                    try:
                        from StringIO import StringIO
                    except ImportError:
                        from io import StringIO

                    stream = StringIO()
                    traceback.print_exc(file=stream)
                    self.send(stream.getvalue())

            def send(self, obj):
                # Send a message to the client
                self.connection.sendall(self.pack_obj(obj))

        # Start the server
        server = Server(ServerHandler)
        server_api = ServerAPI(server)

        assert server.after_bind_socket is not None
        def after_bind_socket(host, port):
            system_mutex.write(str(port))
            if _DEBUG:
                print('debug: Started server at port: %s' % (port,))

        server.after_bind_socket = after_bind_socket
        # Note: not blocking means it'll start in another thread
        server.serve_forever('127.0.0.1', 0, block=True)

    else:
        if _DEBUG:
            with open(system_mutex.filename, 'r') as stream:
                port = stream.read().strip()
            print('debug: Server previously started at port: %s' % (port,))

def stop_server():
    from mu_repo.system_mutex import create_system_mutex_for_current_dir
    system_mutex = create_system_mutex_for_current_dir()
    if not system_mutex.get_mutex_aquired():
        with open(system_mutex.filename, 'r') as stream:
            port = int(stream.read().strip())

        from mu_repo.umsgpack_s_conn import ConnectionHandler, UMsgPacker, Client

        class ClientHandler(ConnectionHandler, UMsgPacker):

            def _handle_decoded(self, decoded):
                print('Warning: not expecting message. Received: %s' % (decoded,))

        client = Client('127.0.0.1', port, ClientHandler)

        if _DEBUG:
            print('debug: client: Killing server')
        client.send('shutdown')

def start_server_in_subprocess():
    import os
    import sys
    import subprocess

    os.path
    env = os.environ.copy()
    env['PYTHONPATH'] = os.environ.get('PYTHONPATH', '') + os.pathsep + os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    subprocess.Popen([sys.executable, __file__], env=env)


if __name__ == '__main__':
    start_server()




