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
import subprocess
import sys




subprocess.call([
    os.path.join(os.path.dirname(sys.executable), 'Scripts', 'mkdocs.exe'),
    'build'],
    cwd=os.path.dirname(__file__),
)
