from pathlib import Path
from typing import Callable

import pytest

import shephex
from shephex import Experiment
from shephex.executor import LocalExecutor
from shephex.experiment import ChainableExperimentIterator, ExperimentContext


def func(a: int, b: int, context: ExperimentContext = None) -> int:
    return a + b

def context_test_func(a: int, context: ExperimentContext = None) -> int:
    if isinstance(context, ExperimentContext):
        return 1 + a
    else:
        return 0

@pytest.fixture(params=['ScriptProcedure', 'PickleProcedure'])
def procedure_type(request: pytest.FixtureRequest) -> str:
    return request.param


@pytest.fixture(params=[False, True])
def context_bool(request: pytest.FixtureRequest) -> bool:
    return request.param


@pytest.fixture(scope='function')
def chain_factory(procedure_type: str, context_bool: bool, tmp_path: Path) -> Callable:
    f = shephex.chain(
        hex_directory=tmp_path, procedure_type=procedure_type, context=context_bool
    )(func)
    return f

@pytest.fixture(scope='function')
def context_chain_factory(procedure_type: str, tmp_path: Path, context_bool: bool) -> Callable:
    f = shephex.chain(
        hex_directory=tmp_path, procedure_type=procedure_type, context=context_bool
    )(context_test_func)
    return f



def test_chain_create(chain_factory: Callable) -> None:
    chain = chain_factory()
    assert isinstance(chain, ChainableExperimentIterator)

def test_chain_execute(chain_factory: Callable) -> None:
    a_ = [1, 2]
    b_ = [2, 4]
    chain = chain_factory()

    experiments = chain.zip(a=a_, b=b_)

    assert len(experiments) == len(a_)
    
    for experiment, a, b in zip(experiments, a_, b_):
        assert isinstance(experiment, Experiment)
        assert experiment.options.kwargs['a'] == a
        assert experiment.options.kwargs['b'] == b

    for experiment in experiments:
        experiment.dump()

    executor = LocalExecutor()
    results = executor.execute(experiments)

    assert len(results) == len(experiments)

    results, options = shephex.result_where(directory=chain.directory)
    for result, option in zip(results, options):
        assert result == option.kwargs['a'] + option.kwargs['b']


def test_chain_with_context_procedure(chain_factory: Callable, context_bool: bool) -> None:
    a_ = [1, 3, 5]
    b_ = [2, 4, 6]
    chain = chain_factory()
    experiments = chain.zip(a=a_, b=b_)

    for experiment in experiments:
        assert experiment.procedure.context is context_bool

def test_chain_with_context_execute(context_chain_factory: Callable, context_bool: bool) -> None:

    chain = context_chain_factory()
    a_ = [1, 3, 5]
    experiments = chain.zip(a=a_)

    for experiment in experiments:
        experiment.dump()

    executor = LocalExecutor()
    results = executor.execute(experiments)

    results, options = shephex.result_where(directory=chain.directory)
    for result, option in zip(results, options):
        if context_bool: 
            assert result == 1 + option.kwargs['a']
        else:
            assert result == 0
