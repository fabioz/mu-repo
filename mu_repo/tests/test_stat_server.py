from __future__ import with_statement
from mu_repo.null import Null
from mu_repo.print_ import PopIgnorePrint, PushIgnorePrint
from mu_repo.rmtree import RmTree
import os.path
import subprocess
import unittest

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



    def test_stat_server(self):
        git = 'git'

        print(os.path.abspath('.'))

        from mu_repo.stat_server.server import ServerAPI
        server_api = ServerAPI(Null)

        subprocess.call([git] + 'init test_temp_dir/remote/projectA'.split(), cwd='.')
        subprocess.call([git] + 'init test_temp_dir/remote/projectB'.split(), cwd='.')
        subprocess.call([git] + 'init test_temp_dir/remote/projectC'.split(), cwd='.')

        print(server_api.stat('git', ['projectA', 'projectB']))
        print(server_api.stat('git', ['projectA', 'projectB']))
        print(server_api.stat('git', ['projectA', 'projectB']))


#===================================================================================================
# main
#===================================================================================================
if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testMuRepo']
    unittest.main()
