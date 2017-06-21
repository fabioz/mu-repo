'''
For developing things are pretty straightforward:

Go into the mkdocs_sources dir and execute

mkdocs.exe serve

Now, for building it's a bit more tricky because it doesn't accept building at the root location),
so, this script should be executed to make the build as it'll create it and relocate to the
appropriate location.

Note: to install mkdocs: pip install mkdocs==0.16.3

To execute must do:

python mkdocs_sources\build_mkdocs.py

(i.e.: must be in the root of the project).
'''

import os
import shutil
import subprocess
import sys


cur_dir = os.path.dirname(__file__)

mkdocs_exe = os.path.join(os.path.dirname(sys.executable), 'Scripts', 'mkdocs.exe')

if not os.path.exists(mkdocs_exe):
    raise AssertionError('Expected %s to exist.' % (mkdocs_exe,))

try:
    args = [mkdocs_exe, 'build', '--clean']
    subprocess.call(args, cwd=cur_dir)
except:
    sys.stderr.write('Error calling: %s\n' % (args,))
    raise

target_dir = os.path.dirname(os.path.dirname(__file__))
site_dir = os.path.join(target_dir, 'site')

for f in os.listdir(site_dir):
    if os.path.isdir(os.path.join(site_dir, f)):
        if os.path.exists(os.path.join(target_dir, f)):
            shutil.rmtree(os.path.join(target_dir, f))

        shutil.copytree(os.path.join(site_dir, f), os.path.join(target_dir, f))
    else:
        shutil.copy(os.path.join(site_dir, f), os.path.join(target_dir, f))
        
