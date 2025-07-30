from click.testing import CliRunner

from shephex.cli.main import cli


def test_main() -> None:
    runner = CliRunner()
    result = runner.invoke(cli)
    assert result.exit_code == 0