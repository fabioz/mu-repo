'''
For developing things are pretty straightforward:

Go into the mkdocs_sources dir and execute

mkdocs.exe serve

Now, for building it's a bit more tricky because it doesn't accept building at the root location),
so, this script should be executed to make the build as it'll create it and relocate to the
appropriate location.

Note: to install mkdocs: pip install mkdocs
'''

import os
import shutil
import subprocess
import sys


subprocess.call([
    os.path.join(os.path.dirname(sys.executable), 'Scripts', 'mkdocs.exe'),
    'build'],
    cwd=os.path.dirname(__file__),
)

target_dir = os.path.dirname(os.path.dirname(__file__))
site_dir = os.path.join(target_dir, 'site')

for f in os.listdir(site_dir):
    if os.path.isdir(os.path.join(site_dir, f)):
        if os.path.exists(os.path.join(target_dir, f)):
            shutil.rmtree(os.path.join(target_dir, f))

        shutil.copytree(os.path.join(site_dir, f), os.path.join(target_dir, f))
    else:
        shutil.copy(os.path.join(site_dir, f), os.path.join(target_dir, f))
        
