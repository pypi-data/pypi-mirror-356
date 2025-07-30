from pathlib import Path
from typing import List

import pytest
from pytest_mock import MockerFixture

from shephex.executor.slurm import SlurmExecutor
from shephex.experiment import Experiment


@pytest.fixture(params=[False, True])
def executor(request: pytest.FixtureRequest, tmpdir: Path) -> SlurmExecutor:
    return SlurmExecutor(ntasks=1, nodes=1, directory=tmpdir, scratch=request.param, safety_check=False)


def test_slurm_executor(executor: SlurmExecutor) -> None:
    assert executor is not None


def test_slurm_executor_submit(
    mocker: MockerFixture, executor: SlurmExecutor, experiments: List[Experiment]
) -> None:
    import subprocess

    mocker.patch('subprocess.run')
    for experiment in experiments:
        experiment.dump()
    executor.execute(experiments)
    assert subprocess.run.called


def test_slurm_executor_submit_single(
    mocker: MockerFixture, executor: SlurmExecutor, experiment_0: Experiment
) -> None:
    import subprocess

    mocker.patch('subprocess.run')
    experiment_0.dump()
    executor.execute(experiment_0)
    assert subprocess.run.called


def test_slurm_executor_single_execute(executor: SlurmExecutor) -> None:
    with pytest.raises(NotImplementedError):
        executor._single_execute()

def test_slurm_executor_dry(
    mocker: MockerFixture, executor: SlurmExecutor, experiments: List[Experiment]
) -> None:
    import subprocess

    mocker.patch('subprocess.run')
    for experiment in experiments:
        experiment.dump()
    executor.execute(experiments, dry=True)
    assert not subprocess.run.called

def test_slurm_executor_empty(
    mocker: MockerFixture, executor: SlurmExecutor
) -> None:
    import subprocess

    mocker.patch('subprocess.run')
    executor.execute([])
    assert not subprocess.run.called

def test_default_directory(tmpdir: Path) -> None:
    executor = SlurmExecutor(ntasks=1, nodes=1, safety_check=False)
    assert executor.directory == Path('slurm')
