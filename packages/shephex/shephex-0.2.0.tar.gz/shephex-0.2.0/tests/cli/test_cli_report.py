import pytest
from click.testing import CliRunner, Result

from shephex import Experiment
from shephex.cli.report import report


@pytest.fixture(scope='module', params=[True, False])
def cli_report_result(request: pytest.FixtureRequest, experiments: list[Experiment]) -> Result:
    experiment_directory = str(experiments[0].root_path)
    runner = CliRunner()
    if request.param:
        result = runner.invoke(report, [experiment_directory, '-l'])
    else:
        result = runner.invoke(report, [experiment_directory, '--total-time', '0.01', '--refresh-rate', '100'])
    return result

def test_cli_report_exit_code(cli_report_result: Result) -> None:
    assert cli_report_result.exit_code == 0

def test_cli_report_identifier(cli_report_result: Result) -> None:
    assert 'identifier' in cli_report_result.output.lower()

def test_cli_report_correct_ids(cli_report_result: Result, experiments: list[Experiment]) -> None:
    print(cli_report_result.output)
    for experiment in experiments:
        assert experiment.identifier in cli_report_result.output