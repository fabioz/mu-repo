from __future__ import with_statement

import os.path
import subprocess

from mu_repo.null import Null


def test_stat_server():
    git = 'git'

    print(os.path.abspath('.'))

    from mu_repo.stat_server.server import ServerAPI
    server_api = ServerAPI(Null)

    subprocess.call([git] + 'init test_temp_dir/remote/projectA'.split(), cwd='.')
    subprocess.call([git] + 'init test_temp_dir/remote/projectB'.split(), cwd='.')
    subprocess.call([git] + 'init test_temp_dir/remote/projectC'.split(), cwd='.')

    print(server_api.stat('git', ['projectA', 'projectB']))
    print(server_api.stat('git', ['projectA', 'projectB']))
    print(server_api.stat('git', ['projectA', 'projectB']))

