from pathlib import Path
from typing import Callable

import pytest

from shephex.experiment import ChainableExperimentIterator, Experiment


@pytest.fixture
def chain_iterator(function: Callable, tmp_path: Path) -> ChainableExperimentIterator:
    return ChainableExperimentIterator(function, directory=tmp_path)

def test_chainable_iterator(chain_iterator: ChainableExperimentIterator) -> None:
    assert chain_iterator is not None

def test_chainable_iterator_initial_length(chain_iterator: ChainableExperimentIterator) -> None:
    assert len(chain_iterator) == 0

def test_chainable_iterator_zip_kwargs_1(chain_iterator: ChainableExperimentIterator) -> None:
    chain_iterator.zip(a=[1, 2, 3], b=[2, 3, 4])
    assert len(chain_iterator) == 3

def test_chainable_iterator_zip_kwargs_2(chain_iterator: ChainableExperimentIterator) -> None:
    chain_iterator.zip(a=[1, 2, 3]).zip(b=[2, 3, 4])
    assert len(chain_iterator) == 3

def test_chainable_iterator_zip_args_1(chain_iterator: ChainableExperimentIterator) -> None:
    chain_iterator.zip([1, 2, 3], [2, 3, 4])
    assert len(chain_iterator) == 3

def test_chainable_iterator_zip_args_2(chain_iterator: ChainableExperimentIterator) -> None:
    chain_iterator.zip([1, 2, 3]).zip([2, 3, 4])
    assert len(chain_iterator) == 3

def test_chainable_iterator_zip_args_kwargs_1(chain_iterator: ChainableExperimentIterator) -> None:
    chain_iterator.zip([1, 2, 3], b=[2, 3, 4])
    assert len(chain_iterator) == 3

def test_chainable_iterator_zip_args_kwargs_2(chain_iterator: ChainableExperimentIterator) -> None:
    chain_iterator.zip([1, 2, 3]).zip(b=[2, 3, 4])
    assert len(chain_iterator) == 3

def test_chainable_iterator_permute_kwargs_1(chain_iterator: ChainableExperimentIterator) -> None:
    chain_iterator.permute(a=[7, 8])
    assert len(chain_iterator) == 2

def test_chainable_iterator_permute_kwargs_2(chain_iterator: ChainableExperimentIterator) -> None:
    chain_iterator.permute(a=[7, 8]).permute(b=[9, 10])
    assert len(chain_iterator) == 4

def test_chainable_iterator_permute_args_1(chain_iterator: ChainableExperimentIterator) -> None:
    chain_iterator.permute([7, 8])
    assert len(chain_iterator) == 2

def test_chainable_iterator_permute_args_2(chain_iterator: ChainableExperimentIterator) -> None:
    chain_iterator.permute([7, 8]).permute([9, 10])
    assert len(chain_iterator) == 4

def test_chainable_iterator_iterate_1(chain_iterator: ChainableExperimentIterator) -> None:
    chain_iterator.zip(a=[1, 2, 3], b=[2, 3, 4]).permute(c=[7, 8])
    for experiment in chain_iterator:
        assert isinstance(experiment, Experiment)
        assert experiment.options['a'] in [1, 2, 3]
        assert experiment.options['b'] in [2, 3, 4]
        assert experiment.options['c'] in [7, 8]

def test_chainable_iterator_iterate_2(chain_iterator: ChainableExperimentIterator) -> None:
    chain_iterator.zip(b=[1, 2, 3]).zip([2, 3, 4])
    assert len(chain_iterator) == 3

    for experiment in chain_iterator:
        assert isinstance(experiment, Experiment)
        assert experiment.options['args'][0] in [2, 3, 4]
        assert experiment.options['b'] in [1, 2, 3]

def test_chainable_iterator_zipped_error_added_options(chain_iterator: ChainableExperimentIterator) -> None:
    with pytest.raises(ValueError):
        chain_iterator.zip(a=[1, 2, 3], b=[2, 3, 4, 3])

def test_chainable_iterator_zipped_error_current_options(chain_iterator: ChainableExperimentIterator) -> None:
    with pytest.raises(ValueError):
        chain_iterator.zip(a=[1, 2, 3]).zip(b=[2, 3, 4, 3])

def test_chainable_iterator_twice_used(chain_iterator: ChainableExperimentIterator) -> None:
    chain_iterator.zip(a=[1, 2, 3], b=[2, 3, 4])
    experiments_1 = []
    for experiment in chain_iterator:
        experiments_1.append(experiment)
    
    experiments_2 = []
    for experiment in chain_iterator:
        experiments_2.append(experiment)

    identifiers_1 = [experiment.identifier for experiment in experiments_1]
    identifiers_2 = [experiment.identifier for experiment in experiments_2]
    assert len(experiments_1) == len(experiments_2)
    for identifier in identifiers_1:
        assert identifier in identifiers_2

def test_chainable_iterator_empty_when_completed(chain_iterator: ChainableExperimentIterator) -> None:
    chain_iterator.zip(a=[1, 2, 3], b=[2, 3, 4])

    for experiment in chain_iterator:
        experiment.update_status('completed')

    count = 0
    for experiment in chain_iterator:
        count += 1

    assert count == 0

def test_chainable_iterator_expected_results(chain_iterator: ChainableExperimentIterator, function: Callable) -> None:
    chain_iterator.zip(a=[1, 2], x=[2, 2])

    result = next(iter(chain_iterator))._execute()
    assert result.result == function(a=1, x=2)

    result = next(iter(chain_iterator))._execute()
    assert result.result == function(a=2, x=2)
