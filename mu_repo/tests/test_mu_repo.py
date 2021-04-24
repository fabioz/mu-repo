'''
Created on May 17, 2012

@author: Fabio Zadrozny
'''
import os.path

from mu_repo import action_diff
import mu_repo
from mu_repo.config import Config


def test_mu_repo():
    contents = '''
    repo=pydev
    repo=studio3
    repo=python-devel
    repo=django
    current_group=pydev-devel
    group=pydev-devel, pydev, studio3
    '''
    config = Config.Create(contents)
    expected_config = mu_repo.Config(
        repos=['pydev', 'studio3', 'python-devel', 'django'],
        current_group='pydev-devel',
        groups={'pydev-devel' : ['pydev', 'studio3'] },
    )
    assert config == expected_config


def test_main():
    status = mu_repo.main(config_file='.bar_file', args=[])
    assert not status.succeeded


def test_serial():
    status = mu_repo.main(config_file='.bar_file', args=['set-var', 'serial=1'])
    assert status.succeeded

    status = mu_repo.main(config_file='.bar_file', args=['get-vars'])
    assert status.config.serial

    status = mu_repo.main(config_file='.bar_file', args=['set-var', 'serial=0'])
    assert status.succeeded

    status = mu_repo.main(config_file='.bar_file', args=['get-vars'])
    assert not status.config.serial


def test_register():
    status = mu_repo.main(config_file='.bar_file', args=[])
    assert not status.succeeded, status.status_message

    status = mu_repo.main(config_file='.bar_file', args=['register', 'pydev'])
    assert status.succeeded

    status = mu_repo.main(config_file='.bar_file', args=['list'])
    assert status.config.repos == ['pydev']

    status = mu_repo.main(config_file='.bar_file', args=['register', 'a', 'b'])
    assert status.succeeded

    status = mu_repo.main(config_file='.bar_file', args=['list'])
    assert status.config.repos == ['a', 'b', 'pydev']


def test_unregister():
    status = mu_repo.main(config_file='.bar_file', args=['register', 'pydev', 'a', 'b'])
    assert status.succeeded

    status = mu_repo.main(config_file='.bar_file', args=['list'])
    assert status.config.repos == ['a', 'b', 'pydev']

    status = mu_repo.main(config_file='.bar_file', args=['unregister', 'a'])
    assert status.succeeded

    status = mu_repo.main(config_file='.bar_file', args=['list'])
    assert status.config.repos == ['b', 'pydev']

    status = mu_repo.main(config_file='.bar_file', args=['unregister', '--all'])
    assert status.succeeded

    status = mu_repo.main(config_file='.bar_file', args=['list'])
    assert status.config.repos == []


def test_action_diff():
    it = action_diff.ParsePorcelain('''R  f2.txt\0f1.txt\0A  f3.txt\0?? .project\0''')
    entries = ','.join([str(x) for x in it])
    assert 'StatusEntry [f2.txt, f1.txt],StatusEntry [f3.txt, f3.txt],StatusEntry [.project, .project]' == \
        entries

    it = action_diff.ParsePorcelain('''R f2.txt\0f1.txt\0A f3.txt\0?? .project\0''')
    entries = ','.join([str(x) for x in it])
    assert 'StatusEntry [f2.txt, f1.txt],StatusEntry [f3.txt, f3.txt],StatusEntry [.project, .project]' == \
        entries


def test_groups():
    status = mu_repo.main(config_file='.bar_file', args=['register', 'pydev'])
    assert status.succeeded
    assert status.config.repos == ['pydev']
    assert status.config.current_group == None
    assert status.config.groups == {}

    # calling group without enough arguments and invalid group
    status = mu_repo.main(config_file='.bar_file', args=['group', 'add'])
    assert not status.succeeded

    status = mu_repo.main(config_file='.bar_file', args=['group', 'rm', 'invalid-group'])
    assert not status.succeeded

    # create group, copying current repos
    status = mu_repo.main(config_file='.bar_file', args=['group', 'add', 'group1'])
    assert status.config.repos == ['pydev']
    assert status.config.current_group == 'group1'
    assert status.config.groups == {'group1' : ['pydev']}

    # create group from scratch and add one repo
    status = mu_repo.main(config_file='.bar_file', args=['group', 'add', 'group2', '--clean'])
    assert status.config.repos == ['pydev']
    assert status.config.current_group == 'group2'
    assert status.config.groups == {'group1' : ['pydev'], 'group2' : []}

    status = mu_repo.main(config_file='.bar_file', args=['register', 'studio3'])
    assert status.config.repos == ['pydev', 'studio3']
    assert status.config.current_group == 'group2'
    assert status.config.groups == {'group1' : ['pydev'], 'group2' : ['studio3']}

    #copy group from pydev
    status = mu_repo.main(config_file='.bar_file', args=['group','add', 'pydev_bugfix', '--copy=group1'])
    assert status.config.repos == ['pydev', 'studio3']
    assert status.config.current_group == 'pydev_bugfix'
    assert status.config.groups == {'group1' : ['pydev'], 'group2' : ['studio3'], 'pydev_bugfix': ['pydev']}


    status = mu_repo.main(config_file='.bar_file', args=['list', '@group1'])
    assert status.config.repos == ['pydev']

    status = mu_repo.main(config_file='.bar_file', args=['list', '@group2'])
    assert status.config.repos == ['studio3']

    # group switch
    status = mu_repo.main(config_file='.bar_file', args=['group', 'switch', 'group1'])
    assert status.config.current_group == 'group1'

    # group del
    status = mu_repo.main(config_file='.bar_file', args=['group', 'del', 'group1'])
    assert status.config.repos == ['pydev', 'studio3']
    assert status.config.current_group == None
    assert status.config.groups == {'group2' : ['studio3'], 'pydev_bugfix': ['pydev']}

    # make sure state is to the rest of the application in other commands

    # switch back to group1 and make sure "list" picks only the repos in that group
    status = mu_repo.main(config_file='.bar_file', args=['group', 'switch', 'group2'])
    assert status.config.current_group == 'group2'

    status = mu_repo.main(config_file='.bar_file', args=['list'])
    assert status.config.repos == ['studio3']
    assert status.config.current_group == 'group2'

    # reset grouping and make sure "list" picks all repos
    status = mu_repo.main(config_file='.bar_file', args=['group', 'reset'])
    assert status.config.current_group == None

    status = mu_repo.main(config_file='.bar_file', args=['list'])
    assert status.config.repos == ['pydev', 'studio3']
    assert status.config.current_group == None

def test_search_config_file_normal_case(workdir):
    """Test config search search works for the usual case up where the file is at the root of the repository."""
    root = os.path.join(workdir, 'project')
    os.makedirs(os.path.join(root, '.git'))

    filename = os.path.join(root, '.mu_repo')
    with open(filename, 'w'):
        pass

    assert mu_repo.SearchConfigDir(root) == root


def test_search_config_file_sub_directories(workdir):
    """Test config dir search finds .mu_repo file in sub-directories."""
    c_dir = os.path.join(workdir, 'a', 'b', 'c')
    os.makedirs(c_dir)

    filename = os.path.join(workdir, 'a', '.mu_repo')
    with open(filename, 'w'):
        pass

    assert mu_repo.SearchConfigDir(os.path.join(workdir, 'a', 'b', 'c')) == os.path.dirname(filename)
    assert mu_repo.SearchConfigDir(os.path.join(workdir, 'a', 'b')) == os.path.dirname(filename)
    assert mu_repo.SearchConfigDir(os.path.join(workdir, 'a')) == os.path.dirname(filename)
    assert mu_repo.SearchConfigDir(workdir) is None

    assert mu_repo.SearchConfigDir(os.path.join(workdir, 'a', 'b', 'c'), recurse_limit=1) is None
    assert mu_repo.SearchConfigDir(os.path.join(workdir, 'a'), recurse_limit=0) == os.path.dirname(filename)

    # a .git repository counts as a config directory
    os.makedirs(os.path.join(workdir, 'a', 'b', '.git'))
    assert mu_repo.SearchConfigDir(os.path.join(workdir, 'a', 'b', 'c')) == os.path.join(workdir, 'a', 'b')
