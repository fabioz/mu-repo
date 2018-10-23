import pytest


@pytest.fixture(autouse=True)
def _setup_and_teardown(tmpdir):
    from mu_repo.print_ import PopIgnorePrint, PushIgnorePrint
    import os
    PushIgnorePrint()
    current = os.path.abspath(os.curdir)
    os.chdir(str(tmpdir))
    yield
    os.chdir(current)
    PopIgnorePrint()


@pytest.fixture
def workdir(tmpdir):
    return str(tmpdir)
