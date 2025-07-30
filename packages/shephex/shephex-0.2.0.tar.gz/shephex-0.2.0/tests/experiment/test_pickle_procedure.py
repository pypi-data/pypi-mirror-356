from pathlib import Path

import pytest

from shephex.experiment.options import Options
from shephex.experiment.procedure import PickleProcedure, Procedure
from shephex.experiment.result import ExperimentError


def f(x: int) -> int:
    if x == 0:
        raise ValueError('x cannot be 0')
    return x


def test_procedure_creation() -> None:
    with pytest.raises(TypeError):
        Procedure()

def test_function_procedure_creation() -> None:
    procedure = PickleProcedure(f)
    assert procedure

def test_function_procedure_execute_success(tmp_path: Path) -> None:
    options = Options(1)
    procedure = PickleProcedure(f)
    result = procedure._execute(options, directory=tmp_path, shephex_directory=tmp_path)
    assert result.status == 'completed'
    assert result.result == 1

def test_function_procedure_execute_fail(tmp_path: Path) -> None:
    options = Options(0)
    procedure = PickleProcedure(f)
    result = procedure._execute(options, directory=tmp_path, shephex_directory=tmp_path)
    assert isinstance(result.result, ExperimentError)
    assert result.status == 'failed'


def test_function_procedure_execute_path(tmpdir: Path) -> None:
    options = Options(1)
    procedure = PickleProcedure(f)
    procedure._execute(options, directory=tmpdir, shephex_directory=tmpdir).result == 1

def test_function_procedure_execute_invalid_context(tmpdir: Path) -> None:
    options = Options(1, context='invalid')
    print(options.kwargs.keys())

    assert 'context' in options.kwargs.keys()
    procedure = PickleProcedure(f)
    with pytest.raises(ValueError):
        procedure._execute(options, directory=tmpdir, context=0, shephex_directory=tmpdir)

def test_function_procedure_execute_context(tmpdir: Path) -> None:
    options = Options(1)    
    procedure = PickleProcedure(f)
    procedure._execute(options, directory=tmpdir, shephex_directory=tmpdir, context=0).result == 1

def test_function_procedure_hash() -> None:
    procedure = PickleProcedure(f)
    assert procedure == PickleProcedure(f)

def test_function_procedure_has_explicit() -> None:
    procedure = PickleProcedure(f)
    hash(procedure) == procedure.hash()


def test_function_procedure_hash_fail() -> None:
    procedure = PickleProcedure(f)
    assert procedure != PickleProcedure(lambda x: x)

def test_function_procedure_dump(tmpdir: Path) -> None:
    procedure = PickleProcedure(f)
    procedure.dump(tmpdir)
    assert (tmpdir / procedure.name).exists()

