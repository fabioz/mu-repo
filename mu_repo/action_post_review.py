from mu_repo.get_repos_and_curr_branch import GetReposAndCurrBranch
from mu_repo.print_ import Print
from mu_repo.repos_with_changes import ComputeReposWithChanges, \
    ComputeReposWithChangesFromCurrentBranchToOrigin
from mu_repo.execute_command import ExecuteCommand


#===================================================================================================
# Run
#===================================================================================================
def Run(params):
    '''
    Submit to reviewboard
    Note: must have already committed the work. 
    
    By default will do a diff from the current_branch to origin/current_branch.
    
    Note: reviewboard must be already configured:
        mu config reviewboard.url http://reviewboard.hdqt.appcelerator.com/
        
    Options:
        #-o: open browser
        #-g: guess description and title
        
    Maybe in the future we could support:
        #--server=http://reviewboard.hdqt.appcelerator.com/
        #--diff-filename=
        
    Should do:
    d:\bin\Python265\Scripts\post-review.exe -g -o --branch=development --tracking-branch=origin/development --bugs-closed=4654 --target-groups=Studio
    
    d:\bin\Python265\Scripts\post-review -g -o --diff-filename=mycode.diff --bugs-closed=4654 --target-groups=Studio
    '''

    args = params.args

    dirty_flag = False
    for arg in args:
        if arg == '--dirty':
            dirty_flag = True
            args.remove(arg)
            break

    if len(args) < 3:
        Print('''Expecting 2 parameters: bugs_closed and target_groups (i.e.: mu post-review 4689 Studio)
Optional: --dirty: to post a review while there are changes in the working dir.''')
        return
    bug_closed = args[1]
    target_group = args[2]

    repos_and_curr_branch = GetReposAndCurrBranch(params)
    repos_with_changes = ComputeReposWithChanges(repos_and_curr_branch, params)

    if not dirty_flag:
        changed = [repo for repo, has_change in repos_with_changes.items() if has_change]
        if changed:
            Print(
                '''Unable to post review. All the contents must be committed before generating a review.
Note: pass '--dirty' flag to commit with changed resources (will still get changes from branch origin/branch).
Changed repos:
%s''' % (' '.join(changed),))
            return

    repos_with_changes = ComputeReposWithChangesFromCurrentBranchToOrigin(repos_and_curr_branch, params)
    if not repos_with_changes:
        Print('Unable to post review. Did not detect change in any repository.')
        return

    Print('Posting review for repos: %s ' % (' '.join(repos_with_changes),))

    as_dict = dict(repos_and_curr_branch)
    for repo in repos_with_changes:
        branch = as_dict[repo]
        try:
            ExecuteCommand(
                [
                    'post-review',
                    '-g',
                    '-o',
                    '--branch=' + branch,
                    '--tracking-branch=origin/' + branch,
                    '--bugs-closed=' + bug_closed,
                    '--target-groups=' + target_group,
                ],
                repo,
                return_stdout=False,
                verbose=True,
            )
        except:
            Print('Some error happened executing the post-review command. Please check if it is in your PATH.')
            return

