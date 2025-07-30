from pathlib import Path
from typing import Callable

import pytest

from shephex import Experiment
from shephex.executor import LocalExecutor
from shephex.experiment import PickleProcedure, ScriptProcedure


def func_function(a: int, b: int) -> int:
    return a + b

@pytest.fixture(params=["script", "function"])
def experiment_factory(request: pytest.FixtureRequest, tmp_path: Path) -> Callable:

    def experiment_factory():

        if request.param == "function":
            procedure = PickleProcedure(func_function)
        elif request.param == "script":
            procedure = ScriptProcedure(func_function)
        a_ = [1, 2, 3] 
        b_ = [4, 5, 6] 

        experiments = []
        expected_results = []
        for a, b in zip(a_, b_):
            experiment = Experiment(procedure=procedure, a=a, b=b, root_path=tmp_path)
            experiments.append(experiment)
            expected_results.append(a + b)

            return experiments, expected_results
    
    return experiment_factory

def test_correct_execution(experiment_factory: Callable) -> None:

    experiments, expected_results = experiment_factory()

    executor = LocalExecutor()
    results = executor.execute(experiments)

    for result, expected_result in zip(results, expected_results):
        assert result.result == expected_result

