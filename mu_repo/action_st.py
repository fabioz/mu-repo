'''
Created on 28/05/2012

@author: Fabio Zadrozny
'''


def ExecuteStCommand(params, repos, git):
    from mu_repo.backwards import iteritems
    from mu_repo.execute_git_command_in_thread import Indent
    from mu_repo.execute_parallel_command import ExecuteInParallel, ParallelCmd
    from mu_repo.get_repos_and_curr_branch import GetReposAndCurrBranch
    from mu_repo.print_ import CreateJoinedReposMsg, Print, RESET_COLOR, START_COLOR
        

    # Do the commands as usual in this process and start the process in a subprocess right afterwards.
    commands = []
    for repo in repos:
        commands.append(ParallelCmd(repo, [git] + ['status', '-s']))

    repos_and_curr_branch = GetReposAndCurrBranch(params, verbose=False)
    as_dict = dict(repos_and_curr_branch)

    empty_repos_and_branches = []
    def OnOutput(output):
        branch_name = as_dict.get(output.repo, 'UNKNOWN_BRANCH')
        if not output.stdout:
            empty_repos_and_branches.append((output.repo, branch_name))
        else:
            status = [
                START_COLOR,
                output.repo,
                ' ',
                branch_name,
                ':',
                RESET_COLOR,
                '\n',
                Indent(output.stdout),
                '\n',
            ]
            Print(''.join(status))

    ExecuteInParallel(commands, on_output=OnOutput)

    if empty_repos_and_branches:
        branch_to_repos = {}
        for repo, branch in empty_repos_and_branches:
            branch_to_repos.setdefault(branch, []).append(repo)

        for branch, repos in iteritems(branch_to_repos):
            Print("${START_COLOR}Unchanged:${RESET_COLOR} %s\nat branch: ${START_COLOR}%s${RESET_COLOR}\n" % (
                CreateJoinedReposMsg('', repos), branch))


#===================================================================================================
# Run
#===================================================================================================
def Run(params):
    '''
    Note: this action always runs in parallel.
    '''
    git = params.config.git
    repos = params.config.repos

    _DEBUG = True

    if _DEBUG:
        import time
        start_time = time.time()

    import sys
    if sys.platform == 'win32':
        from mu_repo.system_mutex import SystemMutex
        # On mu st, we first check if we have a running server
        system_mutex = SystemMutex('.mu_repo_stat_server_port')
        if not system_mutex.get_mutex_aquired():
            with open(system_mutex.filename, 'r') as stream:
                port = int(stream.read().strip())

            # Ok, we have a running server, go on and connect to it!
            from mu_repo.umsgpack_s_conn import ConnectionHandler, UMsgPacker, Client
            import threading

            event = threading.Event()

            class ClientHandler(ConnectionHandler, UMsgPacker):

                def _handle_decoded(self, msgs):
                    if not isinstance(msgs, (tuple, list)):
                        msgs = [msgs]
                    from mu_repo.print_ import Print
                    for msg in msgs:
                        Print(msg)

                    if _DEBUG:
                        print('Total time: %.2fs' % (time.time() - start_time))
                    event.set()

            client = Client('127.0.0.1', port, ClientHandler)

            client.send(('stat', git, repos))
            event.wait(5)
            return

    ExecuteStCommand(params, repos, git)
    if _DEBUG:
        print('Total time: %.2fs' % (time.time() - start_time))

    # After it's properly tested, we should start the server automatically!
    # if sys.platform == 'win32':
    #     if system_mutex.get_mutex_aquired():
    #         system_mutex.release_mutex()
    #         from mu_repo.stat_server import server
    #         server.start_server_in_subprocess()
