import os

import mu_repo
from .utils import push_dir

def set_up(workdir):
    join = os.path.join
    paths = {
            'dir1':  join(workdir, 'projectA', 'sectionX'),
            'dir2':  join(workdir, 'projectB', 'sectionY'),

            'repo1': join(workdir, 'projectA', 'sectionX', 'repo1'),
            'repo2': join(workdir, 'projectB', 'sectionY', 'repo2'),

            'link1': join(workdir, 'projectA', 'sectionX', 'link1'),
            'link2': join(workdir, 'projectB', 'sectionY', 'link2'),
            }

    # Mark repositories
    os.makedirs(join(paths['repo1'], '.git'))
    os.makedirs(join(paths['repo2'], '.git'))

    return paths

def test_direct_symlink(workdir):
    """Linking directly to a repository inside of initial search path"""
    paths = set_up(workdir)
    os.symlink(paths['repo1'], paths['link1'])

    with push_dir('projectA'):
        status = mu_repo.main(config_file='.bar_file', args=['register', '--recursive'])

    assert status.succeeded
    assert status.config.repos == ['sectionX/repo1']

def test_indirect_symlink(workdir):
    """Linking to an ancestor of a repository"""
    paths = set_up(workdir)
    os.symlink(paths['dir1'], paths['link1'])

    with push_dir('projectA'):
        status = mu_repo.main(config_file='.bar_file', args=['register', '--recursive'])

    assert status.succeeded
    assert status.config.repos == ['sectionX/repo1']

def test_search_path_expansion(workdir):
    """Linking to a repository outside of initial search path"""
    paths = set_up(workdir)
    os.symlink(paths['repo2'], paths['link1'])

    with push_dir('projectA'):
        status = mu_repo.main(config_file='.bar_file', args=['register', '--recursive'])

    assert status.succeeded
    assert set(status.config.repos) == set(['sectionX/repo1', '../projectB/sectionY/repo2'])

def test_infinite_cycle(workdir):
    """Linking to own ancestor directory"""
    paths = set_up(workdir)
    os.symlink(paths['dir1'], paths['link1'])

    with push_dir('projectA'):
        status = mu_repo.main(config_file='.bar_file', args=['register', '--recursive'])

    assert status.succeeded
    assert status.config.repos == ['sectionX/repo1']

def test_infinite_cycle_ouside(workdir):
    """Linking to own ancestor directory in expanded search path"""
    paths = set_up(workdir)
    os.symlink(paths['dir2'], paths['link1'])
    os.symlink(paths['dir2'], paths['link2'])

    with push_dir('projectA'):
        status = mu_repo.main(config_file='.bar_file', args=['register', '--recursive'])

    assert status.succeeded
    assert set(status.config.repos) == set(['sectionX/repo1', '../projectB/sectionY/repo2'])
