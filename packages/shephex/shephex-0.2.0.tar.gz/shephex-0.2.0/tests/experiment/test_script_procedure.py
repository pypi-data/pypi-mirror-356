from pathlib import Path

import pytest

from shephex.executor import LocalExecutor
from shephex.experiment import Experiment
from shephex.experiment.procedure import ScriptProcedure

script_body=r"""

import shephex

@shephex.hexperiment()
def hello(a: int, b: int) -> int:
    result = a + b

    with open('hello.txt', 'w') as f:
        f.write(f"Hello, {result}!\n")

    return result
"""

@pytest.fixture
def script(tmpdir: Path) -> Path:

    with open(tmpdir / 'script.py', 'w') as f:
        f.write(script_body)
    return tmpdir / 'script.py'

@pytest.fixture
def procedure(script: Path) -> ScriptProcedure:
    procedure = ScriptProcedure(path=script, function_name='hello')
    return procedure


def test_script_procedure_creation(procedure: ScriptProcedure) -> None:
    assert procedure.script_code == script_body
    assert procedure.function_name == 'hello'


def test_script_procedure_execute(procedure: ScriptProcedure, tmpdir: Path) -> None:
    experiment = Experiment(a=1, b=1, procedure=procedure, root_path=tmpdir)

    executor = LocalExecutor()
    result = executor.execute(experiment)[0]
    assert result.result == 2
    assert (experiment.directory / 'hello.txt').exists()

def test_script_procedure_hash(procedure: ScriptProcedure) -> None:
    assert procedure.hash() == hash(script_body)

def test_script_procedure_dump(procedure: ScriptProcedure, tmpdir: Path) -> None:
    procedure.dump(tmpdir)
    assert (tmpdir / procedure.name).exists()

def test_script_procedure_load(procedure: ScriptProcedure, tmpdir: Path) -> None:
    procedure = ScriptProcedure(script)
    experiment = Experiment(a=1, b=1, procedure=procedure, root_path=tmpdir)
    experiment.dump()
    experiment.load(experiment.directory)