from pathlib import Path
from typing import Callable, List

import pytest

from shephex import Experiment


@pytest.fixture(scope='session')
def function() -> float:
	def func(x: float = 1.0, a: float = 1.0) -> float:
		return a * (x + 1)

	return func

@pytest.fixture(scope='session')
def experiment_factory(function: Callable) -> Callable:
	
    def factory(x: float, a: float, directory: Path) -> Experiment:
        return Experiment(
            x=x,
            a=a,
            function=function,
            root_path=directory,
            status='pending',
        )

    return factory


@pytest.fixture(scope='function')
def experiments(experiment_factory: Callable, tmp_path: Path) -> List[Experiment]:
    return [
        experiment_factory(0, 1, tmp_path),
        experiment_factory(1, 1, tmp_path),
        experiment_factory(2, 1, tmp_path),
    ]

@pytest.fixture(scope='function')
def experiment_0(experiments: List[Experiment]) -> Experiment:
    return experiments[0]

@pytest.fixture(scope='function')
def experiment_1(experiments: List[Experiment]) -> Experiment:
    return experiments[1]

@pytest.fixture(scope='function')
def experiment_2(experiments: List[Experiment]) -> Experiment:
    return experiments[2]
