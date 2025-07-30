from typing import Callable

import pytest

from shephex.experiment.result import ExperimentResult, FutureResult


@pytest.fixture
def experiment_result_factory() -> Callable:
    def experiment_result_factory(result: int, status: str) -> ExperimentResult:
        return ExperimentResult(result, status)
    return experiment_result_factory

@pytest.fixture
def future_result_factory() -> FutureResult:
    return FutureResult

def test_experiment_result(experiment_result_factory: Callable) -> None:
    result = experiment_result_factory(10, "completed")
    assert result.result == 10

def test_experiment_result_status(experiment_result_factory: Callable) -> None:
    result = experiment_result_factory(10, "completed")
    assert result.status == "completed"

def test_experiment_result_status_failed(experiment_result_factory: Callable) -> None:
    result = experiment_result_factory(10, "failed")
    assert result.status == "failed"

def test_experiment_result_status_invalid(experiment_result_factory: Callable) -> None:
    with pytest.raises(ValueError):
        experiment_result_factory(10, "invalid_status")


def test_future_result(future_result_factory: Callable) -> None:
    result = future_result_factory()
    assert result.result is None




