from pathlib import Path
from typing import Callable

import shephex
from shephex.decorators import disable_decorators, get_decorator_state
from shephex.experiment import ChainableExperimentIterator


@shephex.hexperiment()
def function(a: int, b: int) -> int:
    return 1 + a + b

@shephex.chain()
def chained_function(a: int, b: int) -> int:
    return 1 + a + b


def test_decorator_enabled(tmp_path: Path) -> None:

    decorator_state = get_decorator_state()
    decorator_state.enable()
    experiment = function(1, 2)

    assert isinstance(experiment, shephex.Experiment)

def test_decorator_disabled(tmp_path: Path) -> None:
    
    decorator_state = get_decorator_state()
    decorator_state.disable()
    experiment = function()
    decorator_state.enable()

    assert not isinstance(experiment, shephex.Experiment)
    assert isinstance(experiment, Callable)

def test_decorator_context(tmp_path: Path) -> None:
    
    with disable_decorators():
        experiment = function()


    assert not isinstance(experiment, shephex.Experiment)
    assert isinstance(experiment, Callable)


def test_chain_decorator_enabled(tmp_path: Path) -> None:
    
    decorator_state = get_decorator_state()
    decorator_state.enable()
    iterator = chained_function(tmp_path)

    assert isinstance(iterator, ChainableExperimentIterator)

def test_chain_decorator_disabled(tmp_path: Path) -> None:

    with disable_decorators():
        iterator = chained_function(tmp_path)

    assert not isinstance(iterator, ChainableExperimentIterator)
    assert isinstance(iterator, Callable)
    


