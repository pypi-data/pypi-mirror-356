import pytest
from click.testing import CliRunner

from shephex.cli.slurm.slurm import slurm


def test_slurm() -> None:
    runner = CliRunner()
    result = runner.invoke(slurm)
    assert result.exit_code == 0