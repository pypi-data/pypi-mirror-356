import pytest
from click.testing import CliRunner

from shephex.cli.slurm.add_info import add_info
from shephex.experiment import Experiment, ExperimentContext


@pytest.fixture()
def experiment_added_info(experiments: list[Experiment]) -> None:
    directory = experiments[0].directory
    runner = CliRunner()
    runner.invoke(add_info, ['-d', directory, '-j', '1234'])
    return experiments[0]

def test_add_info(experiment_added_info: Experiment) -> None:
    context = ExperimentContext(experiment_added_info.directory / Experiment.shep_dir)
    assert context.meta['job-id'] == '1234'

