import pytest
from click.testing import CliRunner, Result

from shephex import Experiment
from shephex.cli.execute import execute


@pytest.fixture(scope='module', params=[0, 1])
def cli_execute_result(request: pytest.FixtureRequest, experiments: list[Experiment]) -> Result:
    runner = CliRunner()
    index = request.param
    experiment = experiments[index]
    experiment_directory = str(experiment.directory)

    if index == 0:
        result = runner.invoke(execute, [experiment_directory, '-v'])
    else:
        result = runner.invoke(execute, [experiment_directory, '-e', experiment_directory])

    return result

def test_cli_execute_exit_code(cli_execute_result: Result) -> None:
    assert cli_execute_result.exit_code == 0

def test_cli_execute_result_exists(cli_execute_result: Result, experiments: list[Experiment]) -> None:
    result_file = experiments[0].directory / 'shephex' / 'result.pkl'
    assert result_file.exists()

def test_cli_execute_status(cli_execute_result: Result, experiments: list[Experiment]) -> None:
    experiments[0].meta.load(experiments[0].directory / 'shephex')
    assert experiments[0].meta['status'] == 'completed'


