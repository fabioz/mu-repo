import subprocess
from pathlib import Path


import mu_repo


def test_action_default(workdir, monkeypatch):
    workdir = Path(workdir)
    monkeypatch.chdir(workdir)
    # Init two repos: core, and app, with app depending on core.
    subprocess.check_call(['git', 'init', 'core'])
    subprocess.check_call(['git', 'init', 'app'])
    (workdir/ 'app/.mu_repo').write_text("repo=.\nrepo=../core\n", encoding="utf-8")

    # Add a new configuration value only to 'app'.
    monkeypatch.chdir(workdir/ 'app')
    subprocess.check_call(['git', 'config', '--add', 'foo.bar', 'foo-value'])

    # Sanity check we can get the option.
    subprocess.check_call(['git', 'config', '--get', 'foo.bar'])

    # Getting a standard option will work for all repositories.
    status = mu_repo.main(args=['config', '--get', 'core.bare'], config_file='.mu_repo')
    assert status == mu_repo.Status("Finished", succeeded=True)

    # Getting 'foobar' will only work for 'app'.
    status = mu_repo.main(args=['config', '--get', 'foo.bar'], config_file='.mu_repo')
    assert status == mu_repo.Status("Failed:\n  ../core", succeeded=False)


