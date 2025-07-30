from typing import Callable

import pytest


@pytest.fixture(scope='module')
def experiments(tmp_path_factory: Callable, experiment_factory: Callable) -> str:
    tmp_path = str(tmp_path_factory.mktemp('experiment_directory'))

    experiment_0 = experiment_factory(x=0.1, a=2, directory=tmp_path)
    experiment_0.dump()

    experiment_1 = experiment_factory(x=0.2, a=3, directory=tmp_path)
    experiment_1.dump()

    return [experiment_0, experiment_1]