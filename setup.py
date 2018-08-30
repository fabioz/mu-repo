try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='mu_repo',
    version='1.8.0',  # Note: update here and in mu_repo.__init__
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


# For releasing, change version, create tag and push (deploy should be automatic).
# git tag -a mu_repo_1_8_0
# git push --tags
