import subprocess

import mu_repo


def set_up(workdir):
    subprocess.call('git init {}/lib'.format(workdir).split(), cwd='.')
    subprocess.call('git init {}/app'.format(workdir).split(), cwd='.')
    open('{}/lib/dummy'.format(workdir), 'w').close()
    open('{}/app/dummy'.format(workdir), 'w').close()
    with open('{}/.mu_repo'.format(workdir), 'w') as config_file:
        config_file.write('repo=lib\nrepo=app\n')

    # Do an initial commit to create master branch
    mu_repo.main(config_file='.mu_repo', args=['add', '.'])
    mu_repo.main(config_file='.mu_repo', args=['config', '--local', 'user.email', 'you@example'])
    mu_repo.main(config_file='.mu_repo', args=['commit', '-am', '"init"'])


def test_checkout_partial_names(workdir):
    set_up(workdir)
    mu_repo.main(config_file='.mu_repo', args=['branch', 'fb-rock'])
    mu_repo.main(config_file='.mu_repo', args=['branch', 'fb-paper'])
    mu_repo.main(config_file='.mu_repo', args=['branch', 'rb-scissors'])

    # Checkout fb-rock on both projects
    mu_repo.main(config_file='.mu_repo', args=['checkout', 'fb-rock'])
    assert 'fb-rock' == get_current_branch('app')
    assert 'fb-rock' == get_current_branch('lib')

    # Only one possible mathc, switch to rb-scissors
    mu_repo.main(config_file='.mu_repo', args=['checkout', 'rb-'])
    assert 'rb-scissors' == get_current_branch('app')
    assert 'rb-scissors' == get_current_branch('lib')

    # Couldn't guess branch name, do not checkout
    mu_repo.main(config_file='.mu_repo', args=['checkout', 'fb-'])
    assert 'rb-scissors' == get_current_branch('lib')


def get_current_branch(project):
    return subprocess.check_output("git rev-parse --abbrev-ref HEAD".split(), cwd=project).strip().decode()

