from pathlib import Path

import pytest
from pytest_mock import MockerFixture

from shephex.executor.slurm import SlurmBody, SlurmHeader, SlurmScript


@pytest.fixture()
def header() -> SlurmHeader:
    head = SlurmHeader()
    head.add('ntasks', 2)

    return head

@pytest.fixture()
def body() -> SlurmBody:
    body = SlurmBody()
    body.add('echo "Hello World!"')

    return body


def test_slurm_script(tmpdir: Path, header: SlurmHeader, body: SlurmBody) -> None:
    script = SlurmScript(header, body, Path(tmpdir))
    script.write()
    assert script.path.exists()

def test_slurm_script_mock_submit(mocker: MockerFixture, tmpdir: Path, header: SlurmHeader, body: SlurmBody) -> None:
    import subprocess
    mocker.patch('subprocess.run')
    script = SlurmScript(header, body, Path(tmpdir))
    script.submit()
    assert subprocess.run.called

