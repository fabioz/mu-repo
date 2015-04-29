from distutils.core import setup

setup(
    name='mu_repo',
    version='1.0.0',
    description = 'Tool to work with multiple git repositories',
    author='Fabio Zadrozny',
    url='https://github.com/fabioz/mu-repo',
    scripts=['mu'],
    packages=['mu_repo'],
)

# Note: nice reference: https://jamie.curle.io/blog/my-first-experience-adding-package-pypi/
# New version: change version and then:
# python setup.py sdist
# python setup.py sdist upload
