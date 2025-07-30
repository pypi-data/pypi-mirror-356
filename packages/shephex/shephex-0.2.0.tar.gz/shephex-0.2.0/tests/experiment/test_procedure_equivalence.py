
from pathlib import Path
from typing import Callable

import pytest

from shephex import Experiment
from shephex.executor import LocalExecutor
from shephex.experiment import PickleProcedure, ScriptProcedure


def function(a: int, b: int) -> int:
    return a + b

code = """
def function(a: int, b: int) -> int:
    return a + b
"""


@pytest.fixture()
def experiment_factory(tmp_path: Path) -> tuple[Experiment, Experiment]:

    script_proc = ScriptProcedure(code=code, function_name='function')
    script_experiment = Experiment(procedure=script_proc, root_path=tmp_path, a=1, b=1)
    script_experiment.dump()


    function_proc = PickleProcedure(func=function)
    function_experiment = Experiment(procedure=function_proc, root_path=tmp_path, a=1, b=1)
    function_experiment.dump()

    return script_experiment, function_experiment


def test_procedure_equivalence(experiment_factory: Callable) -> None:

    script_exp, function_exp = experiment_factory
    executor = LocalExecutor()

    result_script = executor.execute(script_exp)[0]
    result_function = executor.execute(function_exp)[0]
    assert result_script.result == result_function.result


    
