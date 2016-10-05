try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='mu_repo',
    version='1.4.0',
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
# python setup.py sdist
# python setup.py sdist register upload
