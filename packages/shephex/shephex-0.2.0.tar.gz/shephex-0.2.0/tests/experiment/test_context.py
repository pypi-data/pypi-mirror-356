from pathlib import Path

from shephex.experiment.context import ExperimentContext


def test_experiment_context_creation(tmpdir: Path) -> None:
    context = ExperimentContext(tmpdir)
    assert context

def test_experiment_context_update_progress(tmpdir: Path) -> None:
    context = ExperimentContext(tmpdir)
    context.update_progress("test")
    assert context.meta['progress'] == "test"

def test_experiment_context_update_progress_invalid(tmpdir: Path) -> None:

    context = ExperimentContext(tmpdir)
    context.update_progress(1)
    assert context.meta['progress'] == "1"

def test_experiment_context_repr(tmpdir: Path) -> None:
    context = ExperimentContext(tmpdir)
    assert repr(context) == "ExperimentContext()"
    