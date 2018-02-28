from mu_repo.print_ import PushIgnorePrint, PopIgnorePrint
from mu_repo.rmtree import RmTree
import mu_repo
import os.path
import subprocess
import unittest


#===================================================================================================
# Test
#===================================================================================================
class Test(unittest.TestCase):

    def setUp(self):
        PushIgnorePrint()
        self.clear()
        self.workspace = 'test_temp_dir'
        subprocess.call('git init {}/lib'.format(self.workspace).split(), cwd='.')
        subprocess.call('git init {}/app'.format(self.workspace).split(), cwd='.')
        open('{}/lib/dummy'.format(self.workspace), 'w').close()
        open('{}/app/dummy'.format(self.workspace), 'w').close()
        with open('{}/.mu_repo'.format(self.workspace), 'w') as config_file:
            config_file.write('repo=lib\nrepo=app\n')
        self._last_dir = os.getcwd()
        os.chdir(self.workspace)
        # Do an initial commit to create master branch
        mu_repo.main(config_file='.mu_repo', args=['add', '.'])
        mu_repo.main(config_file='.mu_repo', args=['config', '--local', 'user.email', 'you@example'])
        mu_repo.main(config_file='.mu_repo', args=['commit', '-am', '"init"'])


    def tearDown(self):
        PopIgnorePrint()
        os.chdir(self._last_dir)
        self.clear()

    def clear(self):
        if os.path.exists('test_temp_dir'):
            RmTree('test_temp_dir')

    def test_stat_server(self):
        mu_repo.main(config_file='.mu_repo', args=['branch', 'fb-rock'])
        mu_repo.main(config_file='.mu_repo', args=['branch', 'fb-paper'])
        mu_repo.main(config_file='.mu_repo', args=['branch', 'rb-scissors'])

        # Checkout fb-rock on both projects
        mu_repo.main(config_file='.mu_repo', args=['checkout', 'fb-rock'])
        self.assertEqual('fb-rock', self.get_current_branch('app'))
        self.assertEqual('fb-rock', self.get_current_branch('lib'))

        # Only one possible mathc, switch to rb-scissors
        mu_repo.main(config_file='.mu_repo', args=['checkout', 'rb-'])
        self.assertEqual('rb-scissors', self.get_current_branch('app'))
        self.assertEqual('rb-scissors', self.get_current_branch('lib'))

        # Couldn't guess branch name, do not checkout
        mu_repo.main(config_file='.mu_repo', args=['checkout', 'fb-'])
        self.assertEqual('rb-scissors', self.get_current_branch('lib'))

    def get_current_branch(self, project):
        return subprocess.check_output("git rev-parse --abbrev-ref HEAD".split(), cwd=project).strip().decode()

#===================================================================================================
# main
#===================================================================================================
if __name__ == "__main__":
    unittest.main()
