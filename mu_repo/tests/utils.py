from contextlib import contextmanager
import os.path
import subprocess


def configure_git_user(cwd='.'):
    """
    Configures git with a testing user in the given directory, using local
    config.
    :param cwd: where to execute the git config commands.
    """
    subprocess.check_call('git config user.email testing@test.org',
                          cwd=cwd, shell=True)
    subprocess.check_call('git config user.name Testing', cwd=cwd, shell=True)


@contextmanager
def push_dir(directory):
    old = os.path.realpath(os.path.abspath(os.getcwd()))
    new_dir = os.path.realpath(os.path.abspath(directory))
    assert os.path.exists(new_dir)
    os.chdir(new_dir)
    try:
        yield
    finally:
        os.chdir(old)


