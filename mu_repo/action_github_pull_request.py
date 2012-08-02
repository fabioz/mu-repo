'''
Created on Jun 21, 2012

@author: Fabio Zadrozny
'''
from mu_repo.get_repos_and_curr_branch import GetReposAndCurrBranch
from mu_repo.print_ import Print
from mu_repo.execute_command import ExecuteCommand

#=======================================================================================================================
# Run
#=======================================================================================================================
def Run(params):
    '''
    This action applies a pull request from github in a new branch. There can be no changes in the current repo. 
    
    To execute:
        mu github-pull user/repo.git:branch
    
    Will do the following:
    
        git checkout -b branch-pull-request
        git pull https://github.com/user/repo.git branch
        git checkout initial_branch
        git merge branch-pull-request --no-commit --no-ff
    '''

    config = params.config
    if len(config.repos) != 1:
        Print('Can only apply pull request for a single repo.')
        return

    if len(params.args) < 2:
        Print('Expecting at least 1 argument. E.g.: user/repo.git:branch_to_merge')
        return


    user_repo_and_branch = params.args[1]
    splitted = user_repo_and_branch.split(':')
    if len(splitted) != 2:
        Print('Expected: user/repo.git:branch. Received: %s' % (user_repo_and_branch))
        return
    user_repo, user_branch = splitted
    user = user_repo.split('/')[0]

    repo = iter(config.repos).next()

    git = config.git or 'git'
    cmd = [git, 'status', '--porcelain']
    stdout = ExecuteCommand(cmd, repo, return_stdout=True)

    if stdout:
        Print('Unable to execute because there are changes in the working directory:\n', stdout)
        return


    repos_and_curr_branch = GetReposAndCurrBranch(params)
    if len(repos_and_curr_branch) != 1:
        Print('Must find a single repo with current branch. Found: %s' % (repos_and_curr_branch,))
        return
    _local_repo, local_branch = repos_and_curr_branch[0]

    local_pull_request_branch = user_branch + '-' + user + '-pull-request'

    ExecuteCommand([git, 'checkout', '-b', local_pull_request_branch], '.')
    ExecuteCommand([git, 'pull', 'https://github.com/' + user_repo, user_branch], '.')
#    Exec([git, 'checkout', local_branch])
#    Exec([git, 'merge', local_pull_request_branch, '--no-commit', '--no-ff'])

    msg = '\n'.join([
        '\n$If all went well, do:',
        '${START_COLOR}mu dd${RESET_COLOR} to see changes, then: ',
        '${START_COLOR}mu ac${RESET_COLOR} to commit changes (if all is OK): ',
        'To discard/forget this merge, do:',
        '${START_COLOR}mu reset --hard${RESET_COLOR}',
        '${START_COLOR}mu branch -D %s${RESET_COLOR}' % (local_pull_request_branch,),
        'To merge this request:',
        '${START_COLOR}mu checkout %s${RESET_COLOR}' % (local_branch,),
        '${START_COLOR}mu merge %s --no-commit --no-ff${RESET_COLOR}' % (local_pull_request_branch,),
    ])
    Print(msg)
