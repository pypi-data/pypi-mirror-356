from typing import List

from shephex import Experiment
from shephex.executor import LocalExecutor
from shephex.experiment.result import ExperimentResult


def test_local_executor() -> None:
    executor = LocalExecutor()
    assert executor is not None

def test_local_executor_execute(experiment_0: Experiment) -> None:
    executor = LocalExecutor()
    experiment_0.dump()
    result = executor.execute(experiment_0)[0]
    assert isinstance(result, ExperimentResult)


def test_local_executor_execute_sequence(experiments: List[Experiment]) -> None:
    executor = LocalExecutor()
    for experiment in experiments:
        experiment.dump()

    result = executor.execute(experiments)[0]
    assert isinstance(result, ExperimentResult)

def test_local_executor_dry(experiments: List[Experiment]) -> None:
    executor = LocalExecutor()
    for experiment in experiments:
        experiment.dump()

    executor.execute(experiments, dry=True)[0]
    for experiment in experiments:
        assert experiment.status == 'pending'

