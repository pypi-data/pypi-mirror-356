import pytest
from click.testing import CliRunner

from shephex.cli.slurm.cancel import cancel
from shephex.experiment import Experiment, ExperimentContext, Meta


@pytest.fixture
def running_experiment(experiments: list[Experiment]) -> Experiment:
    exp = experiments[0]
    context = ExperimentContext(directory=exp.directory / Experiment.shep_dir)
    meta = Meta.from_file(exp.directory / Experiment.shep_dir)

    # Imitate a running job
    context.add('job-id', '12345')
    meta['status'] = 'running'
    meta.dump(exp.directory / Experiment.shep_dir)

    return exp

@pytest.fixture()
def non_running_experiment(experiments: list[Experiment]) -> Experiment:
    exp = experiments[1]
    context = ExperimentContext(directory=exp.directory / Experiment.shep_dir)
    meta = Meta.from_file(exp.directory / Experiment.shep_dir)

    # Imitate a non-running job
    context.add('job-id', '12345')
    meta['status'] = 'completed'
    meta.dump(exp.directory / Experiment.shep_dir)

    return exp


def test_running(running_experiment: Experiment) -> None:
    runner = CliRunner()
    result = runner.invoke(cancel, [str(running_experiment.directory), '-p'])
    assert result.exit_code == 0
    assert 'scancel 12345' in result.output

def test_non_running(non_running_experiment: Experiment) -> None:
    runner = CliRunner()
    result = runner.invoke(cancel, [str(non_running_experiment.directory), '-p'])
    assert result.exit_code == 0
    assert 'Job in' in result.output
    assert 'is not running' in result.output
    assert 'No job-ids found' in result.output

    

    