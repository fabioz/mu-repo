'''
Created on May 17, 2012

@author: Fabio Zadrozny
'''
from mu_repo import action_diff
from mu_repo.config import Config
from mu_repo.print_ import PopIgnorePrint, PushIgnorePrint
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

        os.chdir(os.path.dirname(__file__))


    def tearDown(self):
        unittest.TestCase.tearDown(self)
        PopIgnorePrint()
        self.clear()


    def clear(self):
        if os.path.exists('.bar_file'):
            os.remove('.bar_file')


    def testMuRepo(self):
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
        self.assertEqual(config, expected_config)


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
        
        
    def testUnregister(self):
        status = mu_repo.main(config_file='.bar_file', args=['register', 'pydev', 'a', 'b'])
        self.assert_(status.succeeded)
        
        status = mu_repo.main(config_file='.bar_file', args=['list'])
        self.assertEquals(status.config.repos, ['a', 'b', 'pydev'])
        
        status = mu_repo.main(config_file='.bar_file', args=['unregister', 'a'])
        self.assert_(status.succeeded)
        
        status = mu_repo.main(config_file='.bar_file', args=['list'])
        self.assertEquals(status.config.repos, ['b', 'pydev'])
        
        status = mu_repo.main(config_file='.bar_file', args=['unregister', '--all'])
        self.assert_(status.succeeded)
        
        status = mu_repo.main(config_file='.bar_file', args=['list'])
        self.assertEquals(status.config.repos, [])


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
        
        
    def testGroups(self):
        status = mu_repo.main(config_file='.bar_file', args=['register', 'pydev'])
        self.assert_(status.succeeded)
        self.assertEqual(status.config.repos, ['pydev'])
        self.assertEqual(status.config.current_group, None)
        self.assertEqual(status.config.groups, {})

        # calling group without enough arguments and invalid group        
        status = mu_repo.main(config_file='.bar_file', args=['group', 'add'])
        self.assert_(not status.succeeded)
        
        status = mu_repo.main(config_file='.bar_file', args=['group', 'rm', 'invalid-group'])
        self.assert_(not status.succeeded)
        
        # create group, copying current repos
        status = mu_repo.main(config_file='.bar_file', args=['group', 'add', 'group1'])
        self.assertEquals(status.config.repos, ['pydev'])
        self.assertEqual(status.config.current_group, 'group1')
        self.assertEqual(status.config.groups, {'group1' : ['pydev']})
        
        # create group from scratch and add one repo
        status = mu_repo.main(config_file='.bar_file', args=['group', 'add', 'group2', '--clean'])
        self.assertEquals(status.config.repos, ['pydev'])
        self.assertEqual(status.config.current_group, 'group2')
        self.assertEqual(status.config.groups, {'group1' : ['pydev'], 'group2' : []})
        
        status = mu_repo.main(config_file='.bar_file', args=['register', 'studio3'])
        self.assertEquals(status.config.repos, ['pydev', 'studio3'])
        self.assertEqual(status.config.current_group, 'group2')
        self.assertEqual(status.config.groups, {'group1' : ['pydev'], 'group2' : ['studio3']})
        
        # group switch
        status = mu_repo.main(config_file='.bar_file', args=['group', 'switch', 'group1'])
        self.assertEqual(status.config.current_group, 'group1')
        
        # group del
        status = mu_repo.main(config_file='.bar_file', args=['group', 'del', 'group1'])
        self.assertEquals(status.config.repos, ['pydev', 'studio3'])
        self.assertEqual(status.config.current_group, None)
        self.assertEqual(status.config.groups, {'group2' : ['studio3']})
        
        # make sure state is to the rest of the application in other commands
        
        # switch back to group1 and make sure "list" picks only the repos in that group
        status = mu_repo.main(config_file='.bar_file', args=['group', 'switch', 'group2'])
        self.assertEqual(status.config.current_group, 'group2')
        
        status = mu_repo.main(config_file='.bar_file', args=['list'])
        self.assertEquals(status.config.repos, ['studio3'])
        self.assertEqual(status.config.current_group, 'group2')
        
        # reset grouping and make sure "list" picks all repos
        status = mu_repo.main(config_file='.bar_file', args=['group', 'reset'])
        self.assertEqual(status.config.current_group, None)
        
        status = mu_repo.main(config_file='.bar_file', args=['list'])
        self.assertEquals(status.config.repos, ['pydev', 'studio3'])
        self.assertEqual(status.config.current_group, None)
        

#===================================================================================================
# main
#===================================================================================================
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testMuRepo']
    unittest.main()
