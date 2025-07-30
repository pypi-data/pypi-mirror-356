import os # noqa
import pytest
from pathlib import Path


class TemporaryDirectory:

    def __init__(self, tmpdir): # noqa
        self.tmpdir = tmpdir

    def __enter__(self): # noqa
        self.cwd = os.getcwd()
        os.chdir(self.tmpdir)
        print(f'Changed directory to {self.tmpdir}')

    def __exit__(self, exc_type, exc_value, traceback): # noqa
        os.chdir(self.cwd)
        print(f'Changed directory back to {self.cwd}')

@pytest.fixture
def tmpdir_context_manager(tmpdir: Path) -> TemporaryDirectory:
    return TemporaryDirectory(tmpdir)