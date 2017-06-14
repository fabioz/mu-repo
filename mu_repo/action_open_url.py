from mu_repo.print_ import Print

    

#===================================================================================================
# Run
#===================================================================================================
def Run(params):
    '''
    Opens the web-browser to open urls for the modified repositories compared to some 'dest' branch.

    To use:

    mu open-url main-pattern --dest=dest_branch

    The main-pattern may use the following keywords:
        - repo: the repository name
        - source: the source branch
        - dest: the repository destination name


    So, given the following situations, it may be used to create pull requests in:

    On github: https://github.com/user/project/compare/old_development...master

        mu open-url https://github.com/user/{repo}/compare/{source}...{dest} --dest=master

    On bitbucket: https://bitbucket.org/user/project/branch/source_branch?dest=master

        mu open-url https://bitbucket.org/user/{repo}/branch/{source}?dest={dest} --dest=master

    On stash: https://custom.domain.com/stash/projects/container/repos/repo_name/compare/commits?sourceBranch=sourceBranch&targetBranch=master

        mu open-url "https://custom.domain.com/stash/projects/container/repos/{repo}/compare/commits?sourceBranch={source}&targetBranch={dest}" --dest=master

    Note that currently the base url/pattern must be the same for all the repos (it's not possible
    to have one repository hosted in one place and another in another place for the current code
    to work -- for this we'd need to store the url per repository).
    '''

    from mu_repo.get_repos_and_curr_branch import GetReposAndCurrBranch
    from mu_repo.repos_with_changes import ComputeReposWithChangesFromCurrentBranchToOrigin

    repos_and_curr_branch = GetReposAndCurrBranch(params)

    keywords = {}
    if len(params.args) < 2:
        Print("Not enough arguments passed.")
        return
        
    pattern = params.args[1]

    for arg in params.args[2:]:
        if arg.startswith('--'):
            i = arg.index('=')
            key = arg[2:i]
            val = arg[i + 1:]
            keywords[key] = val

        else:
            Print("Unexpected parameter: %s" % (arg,))
            return

    if pattern is None:
        Print("Main pattern not specified.")
        return

    if 'dest' not in keywords:
        Print("--dest= not specified")
        return

    dest = keywords['dest']

    repos_with_changes = set(ComputeReposWithChangesFromCurrentBranchToOrigin(
        repos_and_curr_branch, params, target_branch=dest))


    import webbrowser
    for repo, branch in repos_and_curr_branch:
        keywords['source'] = branch
        if repo in repos_with_changes:
            import os.path
            if repo == '.':
                repo = os.path.basename(os.path.realpath('.'))
            else:
                repo = repo.replace('.', '').replace('/', '').replace('\\', '')
            keywords['repo'] = repo
            url = pattern.format(**keywords)
            webbrowser.open_new_tab(url)
