from pathlib import Path
from typing import Callable

import pytest

from shephex import Experiment, hexperiment
from shephex.executor import LocalExecutor


def func(a: int, b: int) -> int:
    return a + b


@pytest.fixture(params=["PickleProcedure", "ScriptProcedure"])
def hexed_factory(request: pytest.FixtureRequest, tmp_path: Path) -> Callable:
    f = hexperiment(hex_directory=tmp_path, procedure_type=request.param)(func)

    return f

def test_hexperiment_create(hexed_factory: Callable) -> None:
    assert isinstance(hexed_factory(1, 2), Experiment)

def test_hexperiment_execute(hexed_factory: Callable) -> None:

    parameters = [(1, 2), (3, 4), (5, 6)]
    experiments = [hexed_factory(*p) for p in parameters]

    for experiment in experiments:
        assert isinstance(experiment, Experiment)

    for experiment in experiments:
        experiment.dump()

    executor = LocalExecutor()
    results = executor.execute(experiments)

    for result, (a, b) in zip(results, parameters):
        assert result.result == a + b


