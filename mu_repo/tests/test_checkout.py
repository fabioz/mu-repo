import subprocess

import mu_repo
import sys


def set_up(workdir):
    sys.stderr.write('Init 1\n')
    subprocess.call('git init {}/lib'.format(workdir).split(), cwd='.')
    subprocess.call('git config init.defaultBranch master'.split(), cwd='./lib')
    
    sys.stderr.write('Init 2\n')
    subprocess.call('git init {}/app'.format(workdir).split(), cwd='.')
    subprocess.call('git config init.defaultBranch master'.split(), cwd='./app')
    
    sys.stderr.write('Write files\n')
    open('{}/lib/dummy'.format(workdir), 'w').close()
    open('{}/app/dummy'.format(workdir), 'w').close()
    
    sys.stderr.write('Create .mu_repo for both repositories\n')
    with open('{}/.mu_repo'.format(workdir), 'w') as config_file:
        config_file.write('repo=lib\nrepo=app\n')

    # Do an initial commit to create master branch
    sys.stderr.write('Make initial commit.\n')
    mu_repo.main(config_file='.mu_repo', args=['a'])
    mu_repo.main(config_file='.mu_repo', args=['config', '--local', 'user.email', 'you@example'])
    mu_repo.main(config_file='.mu_repo', args=['config', '--local', 'user.name', 'testing'])
    mu_repo.main(config_file='.mu_repo', args=['commit', '--allow-empty', '-n', '-m', 'init'])


def test_checkout_partial_names(workdir):
    set_up(workdir)
    mu_repo.main(config_file='.mu_repo', args=['branch', 'fb-rock'])
    mu_repo.main(config_file='.mu_repo', args=['branch', 'fb-paper'])
    mu_repo.main(config_file='.mu_repo', args=['branch', 'rb-scissors'])

    # Checkout fb-rock on both projects
    status = mu_repo.main(config_file='.mu_repo', args=['checkout', 'fb-rock'])
    assert status == mu_repo.Status("Finished", True)
    assert 'fb-rock' == get_current_branch('app')
    assert 'fb-rock' == get_current_branch('lib')

    # Only one possible mathc, switch to rb-scissors
    status = mu_repo.main(config_file='.mu_repo', args=['checkout', 'rb-'])
    assert status == mu_repo.Status("Finished", True)
    assert 'rb-scissors' == get_current_branch('app')
    assert 'rb-scissors' == get_current_branch('lib')

    # Couldn't guess branch name, do not checkout
    status = mu_repo.main(config_file='.mu_repo', args=['checkout', 'fb-'])
    assert status == mu_repo.Status("ERROR", False)
    assert 'rb-scissors' == get_current_branch('app')
    assert 'rb-scissors' == get_current_branch('lib')


def get_current_branch(project):
    return subprocess.check_output("git rev-parse --abbrev-ref HEAD".split(), cwd=project).strip().decode()

