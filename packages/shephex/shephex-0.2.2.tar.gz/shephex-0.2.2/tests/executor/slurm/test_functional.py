from pathlib import Path

from pytest_mock import MockerFixture

from shephex import Experiment
from shephex.executor.slurm import slurm_execute


def test_slurm_executor_submit(
    mocker: MockerFixture, experiments: list[Experiment], tmpdir: Path
) -> None:
    import subprocess
    mocker.patch('subprocess.run')
    slurm_execute(experiments, directory=tmpdir, safety_check=False)
    assert subprocess.run.called

def test_slurm_executor_submit_config(
    mocker: MockerFixture, experiments: list[Experiment], tmpdir: Path, tmp_config: Path
) -> None:
    import subprocess
    mocker.patch('subprocess.run')
    slurm_execute(experiments, directory=tmpdir, safety_check=False, config=tmp_config)
    assert subprocess.run.called

def test_slurm_executor_submit_profile(
    mocker: MockerFixture, experiments: list[Experiment], tmpdir: Path, tmp_profile: str
) -> None:
    import subprocess
    mocker.patch('subprocess.run')
    slurm_execute(experiments, directory=tmpdir, safety_check=False, profile=tmp_profile)
    assert subprocess.run.called

