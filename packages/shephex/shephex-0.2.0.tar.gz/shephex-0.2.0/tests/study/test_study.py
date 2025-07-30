from pathlib import Path
from typing import Callable, List

import pytest

from shephex import Experiment, Study


@pytest.fixture(scope='function')
def study(tmpdir: Path, experiments: List[Experiment]) -> Study:
    study = Study(tmpdir)
    for experiment in experiments:
        study.add_experiment(experiment)
    return study


def test_study_creation(study: Study) -> None:
    assert study is not None

def test_study_discover(experiment_factory: Callable, tmp_path: Path) -> None:
    experiments = [experiment_factory(x, 1, tmp_path) for x in range(3)]
    study = Study(tmp_path)
    for experiment in experiments:
        study.add_experiment(experiment)
    
    discovered = list(study.discover_experiments())
    for experiment in experiments:
        assert experiment.directory in discovered

def test_study_add_experiment(study: Study, experiment_0: Experiment) -> None:
    study.add_experiment(experiment_0)
    assert study.contains_experiment(experiment_0)

def test_study_add_experiment_no_check(study: Study, experiment_0: Experiment) -> None:
    study.add_experiment(experiment_0, check_contain=False)
    assert study.contains_experiment(experiment_0)

def test_study_update(study: Study, experiment_0: Experiment) -> None:
    experiment_0.status = 'running'
    study.update_experiment(experiment_0)
    assert study.table.where(status='running') == [experiment_0.identifier]

def test_study_refresh(study: Study, experiment_0: Experiment) -> None:
    study.refresh()
    assert study.contains_experiment(experiment_0)

def test_study_refresh_1(experiment_factory: Callable, tmp_path: Path) -> None:
    study = Study(tmp_path)

    for x in range(3):
        experiment = experiment_factory(x, 1, tmp_path)
        experiment.root_path = study.path
        experiment.dump()
    study.refresh(clear_table=True)
    assert study.contains_experiment(experiment)

def test_study_report(study: Study) -> None:
    study.report()

def test_study_get_experiments(study: Study, experiment_0: Experiment) -> None:
    experiments = study.get_experiments(status='all')
    assert experiment_0 in experiments

def test_study_get_experiments_running(study: Study, experiment_0: Experiment) -> None:
    experiment_0.status = 'running'
    study.update_experiment(experiment_0)
    experiments = study.get_experiments(status='running')
    assert experiment_0 in experiments