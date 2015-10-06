from __future__ import with_statement
from contextlib import contextmanager
from mu_repo.print_ import PopIgnorePrint, PushIgnorePrint
from mu_repo.rmtree import RmTree
from os import makedirs
import mu_repo
import os.path
import subprocess
import unittest
from .utils import configure_git_user

#===================================================================================================
# Test
#===================================================================================================
class Test(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
        PushIgnorePrint()
        self.clear()
        self._dirs_stack = []


    def tearDown(self):
        unittest.TestCase.tearDown(self)
        PopIgnorePrint()
        self.clear()


    def clear(self):
        if os.path.exists('test_temp_dir'):
            RmTree('test_temp_dir')


    def read(self, file2):
        with open(file2, 'r') as f:
            return f.read()


    @contextmanager
    def push_dir(self, directory):
        old = os.path.realpath(os.path.abspath(os.getcwd()))
        os.chdir(directory)
        yield
        os.chdir(old)

    def test_clone_with_deps(self):
        git = 'git'

        print(os.path.abspath('.'))

        # Test diffing with new folder structure
        subprocess.call([git] + 'init test_temp_dir/remote/projectA'.split(), cwd='.')
        subprocess.call([git] + 'init test_temp_dir/remote/projectB'.split(), cwd='.')
        subprocess.call([git] + 'init test_temp_dir/remote/projectC'.split(), cwd='.')

        # C depends on B and A
        with open('./test_temp_dir/remote/projectC/.mu_repo', 'w') as stream:
            stream.write('repo=.\nrepo=../projectB\nrepo=../projectA')


        remote_base = os.path.realpath(os.path.abspath('./test_temp_dir/remote'))

        # B depends on A
        with open('./test_temp_dir/remote/projectB/.mu_repo', 'w') as stream:
            stream.write('repo=.\nrepo=../projectA')

        # Commit the changes
        with self.push_dir(remote_base + '/projectB'):
            configure_git_user()
            mu_repo.main(config_file=None, args=['ac', 'Initial commit'])

        with self.push_dir(remote_base + '/projectC'):
            configure_git_user()
            mu_repo.main(config_file=None, args=['ac', 'Initial commit'])

        makedirs('./test_temp_dir/local')
        
        with self.push_dir('./test_temp_dir/local'):
            # git clone C:\bin\mu-repo\test_temp_dir\remote\projectC
            config = mu_repo.Config()
            config.serial = True
            config.remote_hosts = [remote_base]
            mu_repo.main(config_file=None, args=['clone', 'projectC'], config=config)

            assert os.path.exists('projectA/.git')

            assert os.path.exists('projectB/.git')
            assert os.path.exists('projectB/.mu_repo')

            assert os.path.exists('projectC/.git')
            assert os.path.exists('projectC/.mu_repo')
     

    def test_clone_all(self):
        git = 'git'

        print(os.path.abspath('.'))
        
        remote_dir = 'test_temp_dir/remote_clone_all';

        # Test diffing with new folder structure
        subprocess.call([git] + ('init %s/meta_project' % (remote_dir)).split(), cwd='.')
        subprocess.call([git] + ('init %s/projectD' % (remote_dir)).split(), cwd='.')
        subprocess.call([git] + ('init %s/projectE' % (remote_dir)).split(), cwd='.')
        subprocess.call([git] + ('init %s/projectF' % (remote_dir)).split(), cwd='.')

        remote_base = os.path.realpath(os.path.abspath(remote_dir))
        
        # Register meta project repos
        with open('%s/meta_project/.mu_repo' % (remote_dir), 'w') as stream:
            stream.write('repo=projectD\nrepo=projectE\nrepo=projectF\n')
            stream.write('remote_host=%s' % (remote_base))
        
        with self.push_dir(remote_base + '/meta_project'):            
            configure_git_user()
            mu_repo.main(config_file=None, args=['ac', 'Added projects'])
            
        # add some content to A
        with open('%s/projectD/D.txt' % (remote_dir), 'w') as stream:
            stream.write('some content of D')
        # add some content to B
        with open('%s/projectE/E.txt' % (remote_dir), 'w') as stream:
            stream.write('some content of E')
        # add some content to C
        with open('%s/projectF/F.txt' % (remote_dir), 'w') as stream:
            stream.write('some content of F')
        
        # Commit the changes
        with self.push_dir(remote_base + '/projectD'):            
            configure_git_user()
            mu_repo.main(config_file=None, args=['ac', 'Initial commit'])
            
        with self.push_dir(remote_base + '/projectE'):
            configure_git_user()
            mu_repo.main(config_file=None, args=['ac', 'Initial commit'])

        with self.push_dir(remote_base + '/projectF'):
            configure_git_user()
            mu_repo.main(config_file=None, args=['ac', 'Initial commit'])

        makedirs('./test_temp_dir/local_clone_all')
        
        with self.push_dir('./test_temp_dir/local_clone_all'):
            config = mu_repo.Config()
            config.serial = True
            config.remote_hosts = [remote_base]
            mu_repo.main(config_file=None, args=['clone', 'meta_project'], config=config)
            
            with self.push_dir('./meta_project'):
                mu_repo.main(args=['clone', '--all'])
                
                assert os.path.exists('projectD/.git')
                assert os.path.exists('projectD/D.txt')

                assert os.path.exists('projectE/.git')
                assert os.path.exists('projectE/E.txt')

                assert os.path.exists('projectF/.git')
                assert os.path.exists('projectF/F.txt')
             
             
#===================================================================================================
# main
#===================================================================================================
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testMuRepo']
    unittest.main()
           #assert os.path.exists('projectC/.mu_repo')
           