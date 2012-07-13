'''
Created on 27/05/2012

@author: Fabio Zadrozny
'''
from mu_repo.print_ import Print

#===================================================================================================
# Run
#===================================================================================================
def Run(params, add, commit, push):
    args = params.args[1:]
    if commit and not args:
        Print('Message for commit is required for git add -A & git commit -m command.')
        return

    from .action_default import Run #@Reimport
    from mu_repo import Params
    if add:
        Run(Params(params.config, ['add', '-A'], params.config_file))

    if commit:
        Run(Params(params.config, ['commit', '-m', ' '.join(args)], params.config_file))

    if push:
        from mu_repo.get_repos_and_curr_branch import GetReposAndCurrBranch
        from mu_repo.execute_parallel_command import ParallelCmd, ExecuteInParallel

        repos_and_curr_branch = GetReposAndCurrBranch(params)

        commands = list()
        for repo, branch in repos_and_curr_branch:
            commands.append(ParallelCmd(repo, [params.config.git, 'push', 'origin', branch]))

        ExecuteInParallel(commands)

