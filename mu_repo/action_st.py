'''
Created on 28/05/2012

@author: Fabio Zadrozny
'''

def CollectStCacheOnRepos(params, repos, git):
    '''
    Based on ExecuteStCommand.
    '''
    from mu_repo.execute_git_command_in_thread import Indent
    from mu_repo.execute_parallel_command import ExecuteInParallel, ParallelCmd
    from mu_repo.print_ import RESET_COLOR, START_COLOR


    # Do the commands as usual in this process and start the process in a subprocess right afterwards.
    commands = []
    for repo in repos:
        commands.append(ParallelCmd(repo, [git] + ['status', '-s', '-b']))

    repos_to_branch_and_messages = {}
    def OnOutput(output):
        std_output = output.stdout
        split = std_output.split('\n', 1)
        if len(split) > 1:
            branch_name, std_output = split
        else:
            branch_name = std_output
            std_output = ''
        if branch_name.startswith('##'):
            branch_name = branch_name[2:].strip()

        if '...' in branch_name:
            branch_name = branch_name[:branch_name.index('...')]
        if not std_output:
            repos_to_branch_and_messages[output.repo] = (branch_name, '')
        else:
            status = [
                START_COLOR,
                output.repo,
                ' ',
                branch_name,
                ':',
                RESET_COLOR,
                '\n',
                Indent(std_output),
                '\n',
            ]
            repos_to_branch_and_messages[output.repo] = (branch_name, ''.join(status))

    ExecuteInParallel(commands, on_output=OnOutput)
    return repos_to_branch_and_messages


def CreateMessagesFromReposToBranchAndMessages(repos, repos_to_branch_and_messages):
    from mu_repo.backwards import iteritems
    from mu_repo.print_ import CreateJoinedReposMsg

    messages = []
    empty_repos_and_branches = []
    for repo in repos:
        branch, message = repos_to_branch_and_messages.get(
            repo, ('ERROR: Unable to get cache state', 'ERROR: Unable to get cache state'))
        if message:
            messages.append(message)
        else:
            empty_repos_and_branches.append((repo, branch))

    if empty_repos_and_branches:
        branch_to_repos = {}
        for repo, branch in empty_repos_and_branches:
            branch_to_repos.setdefault(branch, []).append(repo)

        for branch, repos in iteritems(branch_to_repos):
            messages.append(
                "${START_COLOR}Unchanged:${RESET_COLOR} %s\nat branch: ${START_COLOR}%s${RESET_COLOR}\n" % (
                CreateJoinedReposMsg('', repos), branch))
    return messages

def ExecuteStCommand(params, repos, git):
    from mu_repo.print_ import Print

    repos_to_branch_and_messages = CollectStCacheOnRepos(params, repos, git)
    for message in CreateMessagesFromReposToBranchAndMessages(repos, repos_to_branch_and_messages):
        Print(message)


#===================================================================================================
# Run
#===================================================================================================
def Run(params):
    '''
    Note: this action always runs in parallel.
    '''
    git = params.config.git
    repos = params.config.repos

    # Note: to time, just pass --timeit in the command line!

    import sys
    if sys.platform == 'win32':
        from mu_repo.system_mutex import create_system_mutex_for_current_dir
        # On mu st, we first check if we have a running server
        system_mutex = create_system_mutex_for_current_dir()
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

                    event.set()

            client = Client('127.0.0.1', port, ClientHandler)

            client.send(('stat', git, repos))
            event.wait(5)
            return

    ExecuteStCommand(params, repos, git)

    # After it's properly tested, we should start the server automatically!
    # if sys.platform == 'win32':
    #     if system_mutex.get_mutex_aquired():
    #         system_mutex.release_mutex()
    #         from mu_repo.stat_server import server
    #         server.start_server_in_subprocess()
