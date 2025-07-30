from pathlib import Path
from typing import List

import pytest

from shephex import Experiment, Study
from shephex.executor import LocalExecutor
from shephex.experiment import ExperimentResult, Options
from shephex.where import id_where, path_where, result_where


@pytest.fixture(scope='function')
def study(tmpdir: Path, experiments: List[Experiment]) -> Study:
    executor = LocalExecutor()
    for experiment in experiments:
        experiment.dump()
    executor.execute(experiments=experiments)

    study = Study(tmpdir)
    for experiment in experiments:
        study.add_experiment(experiment)    
    
    return study

def test_id_where_type(study: Study) -> None:
    ids, options = id_where(directory=study.path)
    assert isinstance(ids[0], str)
    assert isinstance(options[0], Options)


def test_id_where_number(study: Study) -> None:
    ids, options = id_where(directory=study.path)
    assert len(ids) == len(list(study.discover_experiments()))

def test_id_where_condition(study: Study) -> None:
    experiment = study.get_experiments(status='all')[0]
    exp_id_found, options = id_where(**experiment.options, directory=study.path)
    assert experiment.identifier == exp_id_found[0]

def test_id_where_condition_multiple_hits(study: Study) -> None:

    experiments = study.get_experiments(status='all')
    exp_id_found, options = id_where(a=1, directory=study.path)

    for experiment in experiments:
        assert experiment.identifier in exp_id_found

def test_id_where_condition_no_hits(study: Study) -> None:
    exp_id_found, options = id_where(b=1, directory=study.path)
    assert len(exp_id_found) == 0    

def test_path_where_type(study: Study) -> None:
    paths, options = path_where(directory=study.path)
    assert all([isinstance(path, Path) for path in paths])

def test_result_where_type(study: Study) -> None:
    results, options = result_where(directory=study.path, result_object=True)
    assert all([isinstance(result, ExperimentResult) for result in results])

def test_options_match(study: Study) -> None:

    experiments = study.get_experiments(status='all')

    ids, options = id_where(directory=study.path)

    for experiment in experiments:
        id_index = ids.index(experiment.identifier)
        assert experiment.options == options[id_index]






