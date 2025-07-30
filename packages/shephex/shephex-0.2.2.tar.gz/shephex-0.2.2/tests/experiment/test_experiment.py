from pathlib import Path

import pytest

from shephex import Experiment


@pytest.fixture
def experiment(experiment_0: Experiment) -> Experiment:
    return experiment_0

def test_experiment(experiment: Experiment) -> None:
    print(experiment)

def test_experiment_root_path(experiment: Experiment) -> None:
    assert isinstance(experiment.root_path, Path)

@pytest.mark.parametrize('status', ['pending', 'submitted', 'running', 'completed', 'failed'])
def test_experiment_set_valid_status(status: str, experiment: Experiment) -> None:
    experiment.status = status
    assert experiment.status == status

@pytest.mark.parametrize('status', ['invalid', 'status'])
def test_experiment_set_invalid_status(status: str, experiment: Experiment) -> None:
    with pytest.raises(ValueError):
        experiment.status = status

def test_experiment_dump(experiment: Experiment) -> None:
    experiment.dump()
    assert experiment.directory.exists()
    assert experiment.directory.is_dir()

def test_experiment_load(experiment: Experiment) -> None:
    experiment.dump()
    loaded_experiment = Experiment.load(experiment.directory)
    assert loaded_experiment.identifier == experiment.identifier
    assert loaded_experiment.status == experiment.status
    assert loaded_experiment.meta == experiment.meta
    assert loaded_experiment.options == experiment.options
    assert loaded_experiment.directory == experiment.directory
    assert loaded_experiment.root_path == experiment.root_path
    assert loaded_experiment.extension == experiment.extension
    assert loaded_experiment.procedure.hash() == experiment.procedure.hash()

def test_equal_experiments(experiment: Experiment) -> None:
    assert experiment == experiment

def test_unequal_experiments(experiment_0: Experiment, experiment_1: Experiment) -> None:
    assert experiment_0 != experiment_1

def test_experiment_result() -> None:
    with pytest.raises(ValueError):
        Experiment()

def test_experiment_procedure_setter(experiment: Experiment) -> None:
    with pytest.raises(ValueError):
        experiment.procedure = 1

def test_experiment_directory_mkdir(tmpdir: Path) -> None:
    root_path = tmpdir / 'root'
    experiment = Experiment(function=lambda x: x, root_path=root_path)
    experiment.directory    
    experiment.dump()
    assert experiment.directory.exists()

def test_experiment_eq_(experiment: Experiment) -> None:
    assert experiment == experiment

def test_experiment_ne_(experiment_0: Experiment, experiment_1: Experiment) -> None:
    assert experiment_0 != experiment_1

def test_experiment_eq_false(experiment: Experiment) -> None:
    assert experiment != 1

def test_experiment_eq_false_2(experiment: Experiment) -> None:
    other_experiment = Experiment(function=lambda x: x)
    assert experiment != other_experiment

