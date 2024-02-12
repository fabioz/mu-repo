'''
Created on May 23, 2012

@author: Fabio Zadrozny
'''
from __future__ import with_statement

import os.path
import subprocess
import sys

from mu_repo import action_diff, Params
from mu_repo.action_diff import NotifyErrorListeners
from mu_repo.config import Config
from mu_repo.print_ import Print
from mu_repo.rmtree import RmTree

from .utils import configure_git_user

git = r'C:\D\bin\git\bin\git.exe'
if not os.path.exists(git):
    git = 'git'


def _call_diff(branch=None, check_structure=None):
    config = Config(repos=['test_diff_command_git_repo_dir'], git=git)
    params = Params(config, ['dd'] + [branch] if branch else [], config_file=None)

    called = []

    def Call(cmd, *args, **kwargs):
        try:
            if check_structure:
                check_structure()
        except:
            NotifyErrorListeners()
        called.append(cmd[0].lower())

    errors = []

    def OnError(error):
        errors.append(error)

    # Mock things
    original_call = subprocess.call
    subprocess.call = Call
    action_diff.on_errors_listeners.add(OnError)
    try:
        action_diff.Run(params)
    finally:
        action_diff.on_errors_listeners.remove(OnError)
        subprocess.call = original_call
    if errors:
        raise AssertionError('\n\n'.join(errors))
    return called


def test_action_diff():
    temp_dir = 'test_diff_command_git_repo_dir'

    # Test diffing with new folder structure
    subprocess.call([git, 'init', temp_dir], cwd='.')
    configure_git_user(cwd=temp_dir)

    os.mkdir(os.path.join(temp_dir, 'folder1'))
    with open(os.path.join(temp_dir, 'folder1', 'out.txt'), 'w') as f:
        f.write('out')
    called = _call_diff()
    if sys.platform.startswith('win'):
        merge_command = 'winmergeu.exe'
    else:
        merge_command = 'bcomp'
    assert [merge_command] == called

    # Test diffing with previous version of HEAD without changes
    subprocess.check_call([git] + 'add -A'.split(), cwd=temp_dir)
    subprocess.check_call([git] + 'commit -m "Second'.split(), cwd=temp_dir)
    called = _call_diff()
    assert [] == called  # Not called as we don't have any changes.

    # Test diffing with previous version of HEAD~1
    def check_structure():
        prev = os.path.join('.mu.diff.git.tmp', 'REPO', 'test_diff_command_git_repo_dir', 'folder1', 'out.txt')
        curr = os.path.join('.mu.diff.git.tmp', 'WORKING', 'test_diff_command_git_repo_dir', 'folder1', 'out.txt')
        assert os.path.exists(prev)
        assert os.path.exists(curr)
        Print('prev', open(prev, 'r').read())
        Print('curr', open(curr, 'r').read())

    with open(os.path.join(temp_dir, 'folder1', 'out.txt'), 'w') as f:
        f.write('new out')
    subprocess.check_call([git] + 'add -A'.split(), cwd=temp_dir)
    subprocess.check_call([git] + 'commit -m "Second'.split(), cwd=temp_dir)
    called = _call_diff('HEAD~1', check_structure=check_structure)
    assert [merge_command] == called

    # Test diffing dir structure in git changed for file in working dir
    # Nothing changed at this point: newest git now gives a non-zero value in
    # such a case if we try to commit.
    # subprocess.check_call([git] + 'add -A'.split(), cwd=temp_dir)
    # subprocess.check_call([git] + 'commit -m "Third'.split(), cwd=temp_dir)
    RmTree(os.path.join(temp_dir, 'folder1'))
    with open(os.path.join(temp_dir, 'folder1'), 'w') as f:
        f.write('folder1 is now file.')

    called = _call_diff()
    assert [merge_command] == called

    # Do mu st/mu up just to check if it works.
    from mu_repo.action_default import Run
    config = Config(repos=[temp_dir], git=git)
    Run(Params(config, ['st'], config_file=None))

    import mu_repo
    mu_repo.main(config_file=None, args=['up'])

