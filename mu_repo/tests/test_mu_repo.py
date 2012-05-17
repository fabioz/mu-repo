'''
Created on May 17, 2012

@author: Fabio Zadrozny
'''
import unittest
import mu_repo
import os.path
from StringIO import StringIO


#===================================================================================================
# Test
#===================================================================================================
class Test(unittest.TestCase):


    def setUp(self):
        unittest.TestCase.setUp(self)
        self.clear()


    def tearDown(self):
        unittest.TestCase.tearDown(self)
        self.clear()


    def clear(self):
        if os.path.exists('.bar_file'):
            os.remove('.bar_file')


    def testMuRepo(self):
        contents = '''repo=pydev
repo=studio3
'''
        config = mu_repo.ParseConfig(contents)
        self.assertEqual(config, mu_repo.Config(repos=['pydev', 'studio3']))


    def testMain(self):
        status = mu_repo.main(config_file='.bar_file', stream=StringIO())
        self.assert_(not status.succeeded)


    def testRegister(self):
        status = mu_repo.main(config_file='.bar_file', stream=StringIO())
        self.assert_(not status.succeeded)

        status = mu_repo.main(config_file='.bar_file', args=['register', 'pydev'], stream=StringIO())
        self.assert_(status.succeeded)

        status = mu_repo.main(config_file='.bar_file', args=['list'], stream=StringIO())
        self.assertEquals(status.config['repos'], ['pydev'])

        status = mu_repo.main(config_file='.bar_file', args=['register', 'a', 'b'], stream=StringIO())
        self.assert_(status.succeeded)

        status = mu_repo.main(config_file='.bar_file', args=['list'], stream=StringIO())
        self.assertEquals(status.config['repos'], ['pydev', 'a', 'b'])


#===================================================================================================
# main
#===================================================================================================
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testMuRepo']
    unittest.main()
