from mu_repo.execute_command import ExecuteCommand
from mu_repo.print_ import Print
import os

#===================================================================================================
# Run
#===================================================================================================
def Run(params):
    '''
    Usage: 
      Cloning one or multiple registered repositories
      $mu clone repo-name [repo-name] ...
      
      Cloning all registered repositories
      $mu clone --all
    
    mu-repo can deal with cloning a repository and other referenced repositories recursively.

    To work this way, users are expected to commit the .mu_repo files they rely on and set
    the base urls that users work with.

    i.e.:

    Say that someone is working with 3 projects: A, B and C and C depends on B and B depends on A
    and they're all available on https://github.com/myuser

    The urls in this case to be checked out would be something as:

    ssh://git@github.com:myuser/projectA.git

    https://github.com/myuser/projectA.git

    So, the url: https://github.com/myuser or git@github.com:myuser has to be configured as the
    'base' url for clones.

    mu-repo in this case will work with git to provide that configuration, so, one should first
    add that remote for mu-repo to work with:

    git config --global --add mu-repo.remote-base-url ssh://git@github.com:myuser

    Note that it's possible to add as many urls as wanted.

    To check what are the actual urls that mu-repo will use (and the order in which they'll be
    tried, it's possible to do):

    git config --get-regexp mu-repo.remote-base-url
    '''

    args = params.args
    assert args[0] == 'clone'
    args = args[1:]
    
    repos = []
    other_cmd_line_args = []
    
    if len(args) == 1 and args[0] == '--help':
        import webbrowser
        webbrowser.open("http://fabioz.github.io/mu-repo/cloning/")
        Print('Opening http://fabioz.github.io/mu-repo/cloning/ for help on cloning...')
        return        
    elif len(args) == 1 and args[0] == '--all':
        Print("Cloning all registered repos...")
        repos = params.config.repos
    else:
        for arg in args:
            if not arg.startswith('-') and not '@' in arg and not ':' in arg and not '/' in arg:
                repos.append(arg)
            else:
                other_cmd_line_args.append(arg)

    remote_hosts = params.config.remote_hosts

    if not repos:
        Print('Unable to clone because the repository name for cloning with mu was not detected.')
        return


    if not remote_hosts:
        Print(
            'No mu-repo.remote-base-url specified for mu to work with.\n'
            'Please specify the remote hosts for cloning with mu. i.e.:\n'
            '\n'
            'git config --global --add mu-repo.remote-base-url ssh://git@github.com:myuser'
        )
        return

    Print('Working with remote hosts:')
    for host in remote_hosts:
        Print('    %s' % host)
    Print('')


    # If we got here we have a name which we should be able to concatenate with one of our base
    # remotes

    import mu_repo

    for repo in repos:
        for remote in remote_hosts:
            # Check if the directory was created (and is a git repository)
            if _Clone(remote, repo, params, other_cmd_line_args):
                # Ok, it exists, let's grab the dependencies (if there are any)
                created_dir = os.path.join('.', repo)
                new_mu_repo = os.path.join(created_dir, '.mu_repo')
                if os.path.exists(new_mu_repo):

                    with open(os.path.join(new_mu_repo), 'r') as stream:
                        mu_config = mu_repo.Config.Create(stream.read())

                    for new_repo in mu_config.repos:
                        if new_repo in ('.', './', '.\\'):
                            continue

                        if not new_repo.startswith('../') and not new_repo.startswith('..\\'):
                            Print('Cannot clone: ${START_COLOR}%s${RESET_COLOR} (currently only works with relative repositories matching: ../name or ..\\name)' % (new_repo,))
                        else:
                            # I.e.: can only clone repositories that would appear alongside
                            # the repository just cloned.
                            new_repo_name = new_repo[3:]
                            if new_repo_name and new_repo_name[0] not in ('.', '/', '\\'):
                                # Ok, seems like something valid for us to clone in the current dir
                                # (along what we just cloned)

                                # Create a copy and reorder so that the current one appears first.
                                check_at = remote_hosts[:]
                                check_at.remove(remote)
                                check_at = [remote] + check_at

                                for remote in check_at:
                                    if _Clone(remote, new_repo_name, params, other_cmd_line_args):
                                        # Ok, worked for this repo
                                        break
                            else:
                                Print('Cannot clone: ${START_COLOR}%s${RESET_COLOR} (currently only works with relative repositories matching: ../name or ..\\name)' % (new_repo,))

                # Ok, we did the work for this repo (go on to the next)
                break


def _Clone(remote, repo, params, other_cmd_line_args):
    created_dir = os.path.join('.', repo)
    if os.path.exists(os.path.join(created_dir, '.git')):
        # If it already exists, bail out!
        Print('Skipping clone of: ${START_COLOR}%s${RESET_COLOR} because it already exists.' % (repo,))
        return True

    remote_path = remote
    if not remote_path.endswith('/') and not remote_path.endswith('\\'):
        remote_path += '/'

    git = params.config.git
    ExecuteCommand([git, 'clone', '%s%s' % (remote_path, repo)] + other_cmd_line_args, '.')
    if os.path.exists(os.path.join(created_dir, '.git')):
        return True
    return False



