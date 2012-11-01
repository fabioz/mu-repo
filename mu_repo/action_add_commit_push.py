'''
Created on 27/05/2012

@author: Fabio Zadrozny
'''

#===================================================================================================
# Run
#===================================================================================================
def Run(params, add, commit, push):
    from .print_ import Print, CreateJoinedReposMsg

    args = params.args[1:]
    if commit and not args:
        Print('Message for commit is required for git add -A & git commit -m command.')
        return

    from .execute_parallel_command import ParallelCmd, ExecuteInParallelStackingMessages

    serial = params.config.serial
    if add:
        commands = [ParallelCmd(repo, [params.config.git, 'add', '-A']) for repo in params.config.repos]
        ExecuteInParallelStackingMessages(
            commands,
            lambda output: not output.stdout.strip(),
            lambda repos: Print(CreateJoinedReposMsg('Executed "git add -A" in:', repos)),
            serial=serial,
        )


    if commit:
        commit_msg = ' '.join(args)
        commands = [ParallelCmd(repo, [params.config.git, 'commit', '-m', commit_msg])
            for repo in params.config.repos]

        ExecuteInParallelStackingMessages(
            commands,
            lambda output: 'nothing to commit (working directory clean)' in output.stdout,
            lambda repos: Print(CreateJoinedReposMsg('Nothing to commit at:', repos)),
            serial=serial,
        )


    if push:
        from .get_repos_and_curr_branch import GetReposAndCurrBranch
        repos_and_curr_branch = GetReposAndCurrBranch(params)

        commands = [ParallelCmd(repo, [params.config.git, 'push', 'origin', branch])
            for (repo, branch) in repos_and_curr_branch]

        ExecuteInParallelStackingMessages(
            commands,
            lambda output: not output.stdout.strip() and output.stderr.strip() == 'Everything up-to-date',
            lambda repos: Print(CreateJoinedReposMsg('Up-to-date:', repos)),
            serial=serial,
        )
