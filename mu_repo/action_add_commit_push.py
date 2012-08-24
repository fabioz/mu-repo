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

    from .action_default import Run #@Reimport
    from . import Params

    if add:
        repos = []
        def on_output(output):
            if output.stdout:
                Print(output)
            else:
                repos.append(output.repo)
        Run(Params(params.config, ['add', '-A'], params.config_file), on_output)
        if repos:
            Print(CreateJoinedReposMsg('Executed "git add -A" in:', repos))

    if commit:
        Run(Params(params.config, ['commit', '-m', ' '.join(args)], params.config_file))


    if push:
        from .get_repos_and_curr_branch import GetReposAndCurrBranch
        from .execute_parallel_command import ParallelCmd, ExecuteInParallelStackingMessages

        repos_and_curr_branch = GetReposAndCurrBranch(params)

        commands = list()
        for repo, branch in repos_and_curr_branch:
            commands.append(ParallelCmd(repo, [params.config.git, 'push', 'origin', branch]))

        ExecuteInParallelStackingMessages(
            commands,
            lambda output: not output.stdout.strip() and output.stderr.strip() == 'Everything up-to-date',
            lambda repos: Print(CreateJoinedReposMsg('Up-to-date:', repos))
        )
