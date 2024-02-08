import subprocess
from pathlib import Path


import mu_repo


def test_action_default(workdir, monkeypatch):
    workdir = Path(workdir)
    monkeypatch.chdir(workdir)
    subprocess.check_call(f'git init core')
    subprocess.check_call(f'git init app')
    (workdir/ 'app/.mu_repo').write_text("repo=.\nrepo=../core\n", encoding="utf-8")

    monkeypatch.chdir(workdir/ 'app')
    subprocess.check_call(f'git config --add foo.bar foo-value')

    subprocess.check_call(f'git config --get foo.bar')

    status = mu_repo.main(args=['config', '--get', 'core.bare'], config_file='.mu_repo')
    assert status == mu_repo.Status("Finished", succeeded=True)

    status = mu_repo.main(args=['config', '--get', 'foo.bar'], config_file='.mu_repo')
    assert status == mu_repo.Status("Failed:\n  ../core", succeeded=False)


