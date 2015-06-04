from mu_repo.print_ import Print
from mu_repo.execute_command import ExecuteCommand

#===================================================================================================
# Run
#===================================================================================================
def Run(params):
    '''
    This action will grab the latest version of mu-repo from the repository.
    '''
    import mu_repo
    import os.path
    repo_dir = os.path.dirname(os.path.dirname(mu_repo.__file__))
    if not os.path.exists(os.path.join(repo_dir, '.git')):
        Print(
            'Can only automatically update mu-repo if it was properly gotten from a git repository '
            '(if it was installed with pip, use ${START_COLOR}pip install mu-repo --upgrade${RESET_COLOR}).'
        )
        return

    config = params.config
    git = config.git or 'git'
    ExecuteCommand([git, 'pull', '--rebase'], repo=repo_dir)
