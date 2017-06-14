try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='mu_repo',
    version='1.6.0',  # Note: update here and in mu_repo.__init__
    description = 'Tool to work with multiple git repositories',
    author='Fabio Zadrozny',
    url='http://fabioz.github.io/mu-repo',
    # scripts=['mu'], -- entry_points:console_scripts should do what we want.
    packages=['mu_repo'],
    
    entry_points = {
        'console_scripts': [
            'mu = mu_repo:main_entry_point',                  
        ],
    },
)

# Note: nice reference: https://jamie.curle.io/blog/my-first-experience-adding-package-pypi/
# New version: change version and then:
# git tag -a mu_repo_1_5_0
# git push --tags
# python setup.py sdist
# python setup.py sdist upload

#
# Note: Upload may fail if ~/.pypirc is not present with username (see: https://github.com/pypa/setuptools/issues/941)
# Contents of ~/.pypirc:
#
# [distutils]
# index-servers =
#     pypi
#
# [pypi]
# repository: https://upload.pypi.org/legacy/
# username: <username>

