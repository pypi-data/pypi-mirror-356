import pytest
from click.testing import CliRunner, Result

from shephex import Experiment
from shephex.cli.report import report


@pytest.fixture(scope='module', params=[0, 1, 2, 3, 4])
def cli_report_result(request: pytest.FixtureRequest, experiments: list[Experiment]) -> Result:
    experiment_directory = str(experiments[0].root_path)
    runner = CliRunner()
    if request.param == 0:
        result = runner.invoke(report, [experiment_directory, '-l'])
    elif request.param == 1:
        result = runner.invoke(report, [experiment_directory, '--total-time', '0.01', '--refresh-rate', '100'])
    elif request.param == 2:
        result = runner.invoke(report, [experiment_directory, '-l', '-f', 'status', 'pending', 'str'])
    elif request.param == 3:
        result = runner.invoke(report, [experiment_directory, '-l', '-fr', 'x', '0.0', '5.0'])
    elif request.param == 4:
        result = runner.invoke(report, [experiment_directory, '-l', '-f', 'status', 'completed,pending', 'str'])

    return result

def test_cli_report_exit_code(cli_report_result: Result) -> None:
    assert cli_report_result.exit_code == 0

def test_cli_report_identifier(cli_report_result: Result) -> None:
    assert 'identifier' in cli_report_result.output.lower()

def test_cli_report_correct_ids(cli_report_result: Result, experiments: list[Experiment]) -> None:
    print(cli_report_result.output)
    for experiment in experiments:
        assert experiment.identifier in cli_report_result.output