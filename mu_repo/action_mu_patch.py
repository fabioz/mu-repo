from mu_repo.get_repos_and_curr_branch import GetReposAndCurrBranch

#===================================================================================================
# Run
#===================================================================================================
def Run(params):
    '''
    This action will create diff files suitable for review board (i.e.: the actual patch with 
    added but uncommitted work and a parent patch to be used with the difference from the current
    branch to the remote branch). 
    '''
    from mu_repo.print_ import Print
    from . import action_add_commit_push
    from mu_repo.execute_parallel_command import ParallelCmd, ExecuteInParallel
    import os.path


    remove = []
    for f in os.listdir('.'):
        if os.path.isfile(f) and f.endswith('.patch') and f.startswith('__diff__.'):
            remove.append(f)
    if remove:
        n = ''
        while n not in ('y', 'n'):
            n = raw_input(
                'Is it OK to remove previous diff files: %s\nDelete and continue (y) or cancel (n)? ' %
                ', '.join(remove)).strip().lower()

            if n == 'y':
                for f in remove:
                    os.remove(f)
                break
            if n == 'n':
                Print('Canceling mu-patch action.')
                return

    #1. Adds all before doing the action
    action_add_commit_push.Run(params, add=True, commit=False, push=False)
    Print('') #add new line


    #2. Create a diff with the current changes.
    empty_diff_repos = set()
    diffed_repos = []
    def OnOutput(output):
        stdout = output.stdout
        if stdout.strip():
            diffed_repos.append(output.repo)
            filename = '__diff__.' + output.repo + '.patch'
            Print('Writing diff --cached: ', filename)
            with open(filename, 'w') as f:
                f.write(stdout)
        else:
            empty_diff_repos.add(output.repo)

    commands = [ParallelCmd(repo, [params.config.git, 'diff', '--cached', '--full-index'])
        for repo in params.config.repos]
    ExecuteInParallel(commands, on_output=OnOutput, serial=False)

    #3. Create a parent diff
    def OnOutput(output): #@DuplicatedSignature
        stdout = output.stdout
        if stdout.strip():
            filename = '__diff__.parent.' + output.repo + '.patch'
            Print('Writing parent diff  : ', filename)
            with open(filename, 'w') as f:
                f.write(stdout)

    previous_repos = params.config.repos
    params.config.repos = diffed_repos
    try:
        repos_and_curr_branch = GetReposAndCurrBranch(params, verbose=False)
        #git diff origin/development development
        commands = [ParallelCmd(repo, [params.config.git, 'diff', 'origin/%s' % branch, '%s' % branch])
            for (repo, branch) in repos_and_curr_branch]
        #Always in parallel
        ExecuteInParallel(commands, on_output=OnOutput, serial=False)
    finally:
        params.config.repos = previous_repos


    if empty_diff_repos:
        Print('\nNote: empty diffs --cached for: ', ', '.join(sorted(empty_diff_repos)))



