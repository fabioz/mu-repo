try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='mu_repo',
    version='1.8.1',  # Note: update here and in mu_repo.__init__
    description = 'Tool to work with multiple git repositories',
    long_description = '''mu-repo enables dealing with multiple git and provides features such as:

* Cloning multiple repositories
* Creating groups of repositories
* Diffing changes for edition with WinMerge or meld.
* Checking out branches by partial name matching.
* Preview incoming changes on current branch.
* Shortcuts for common git operations.
* Open Url for opening the browser to create pull requests over multiple repositories.
* Run **arbitrary commands** on registered repositories.

See: http://fabioz.github.io/mu-repo for more information.
''',
    long_description_content_type="text/markdown",
    author='Fabio Zadrozny',
    url='http://fabioz.github.io/mu-repo',
    # scripts=['mu'], -- entry_points:console_scripts should do what we want.
    packages=['mu_repo'],
    classifiers=[
        'Development Status :: 6 - Mature',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Version Control',
    ],
    entry_points = {
        'console_scripts': [
            'mu = mu_repo:main_entry_point',                  
        ],
    },
)


# For releasing, change version, create tag and push (deploy should be automatic).
# git tag -a mu_repo_1_8_1
# git push --tags
