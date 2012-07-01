'''
Created on May 17, 2012

@author: Fabio Zadrozny
'''
from mu_repo import action_diff
from mu_repo.config import Config
from mu_repo.print_ import PushIgnorePrint, PopIgnorePrint
import mu_repo
import os.path
import unittest


#===================================================================================================
# Test
#===================================================================================================
class Test(unittest.TestCase):


    def setUp(self):
        unittest.TestCase.setUp(self)
        PushIgnorePrint()
        self.clear()


    def tearDown(self):
        unittest.TestCase.tearDown(self)
        PopIgnorePrint()
        self.clear()


    def clear(self):
        if os.path.exists('.bar_file'):
            os.remove('.bar_file')


    def testMuRepo(self):
        contents = '''repo=pydev
repo=studio3
'''
        config = Config.Create(contents)
        self.assertEqual(config, mu_repo.Config(repos=['pydev', 'studio3']))


    def testMain(self):
        status = mu_repo.main(config_file='.bar_file', args=[])
        self.assert_(not status.succeeded)


    def testSerial(self):
        status = mu_repo.main(config_file='.bar_file', args=['set-var', 'serial=1'])
        self.assert_(status.succeeded)

        status = mu_repo.main(config_file='.bar_file', args=['get-vars'])
        self.assert_(status.config.serial)

        status = mu_repo.main(config_file='.bar_file', args=['set-var', 'serial=0'])
        self.assert_(status.succeeded)

        status = mu_repo.main(config_file='.bar_file', args=['get-vars'])
        self.assert_(not status.config.serial)


    def testRegister(self):
        status = mu_repo.main(config_file='.bar_file', args=[])
        self.assert_(not status.succeeded, status.status_message)

        status = mu_repo.main(config_file='.bar_file', args=['register', 'pydev'])
        self.assert_(status.succeeded)

        status = mu_repo.main(config_file='.bar_file', args=['list'])
        self.assertEquals(status.config.repos, ['pydev'])

        status = mu_repo.main(config_file='.bar_file', args=['register', 'a', 'b'])
        self.assert_(status.succeeded)

        status = mu_repo.main(config_file='.bar_file', args=['list'])
        self.assertEquals(status.config.repos, ['a', 'b', 'pydev'])


    def testActionDiff(self):
        it = action_diff.ParsePorcelain('''R  f2.txt\0f1.txt\0A  f3.txt\0?? .project\0''')
        entries = ','.join([str(x) for x in it])
        self.assertEqual(
            'StatusEntry [f2.txt, f1.txt],StatusEntry [f3.txt, f3.txt],StatusEntry [.project, .project]',
            entries
        )

        it = action_diff.ParsePorcelain('''R f2.txt\0f1.txt\0A f3.txt\0?? .project\0''')
        entries = ','.join([str(x) for x in it])
        self.assertEqual(
            'StatusEntry [f2.txt, f1.txt],StatusEntry [f3.txt, f3.txt],StatusEntry [.project, .project]',
            entries
        )

#===================================================================================================
# main
#===================================================================================================
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testMuRepo']
    unittest.main()
