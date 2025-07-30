from pathlib import Path

import pytest
from click.testing import CliRunner

from shephex.cli.slurm.profile import (
    add,
    delete,
    directory,
    list_profiles,
    print_profile,
    profile,
)
from shephex.executor.slurm.slurm_profile import SlurmProfileManager


def test_profile() -> None:
    runner = CliRunner()
    result = runner.invoke(profile)
    assert result.exit_code == 0


def test_list() -> None:
    runner = CliRunner()
    result = runner.invoke(list_profiles)
    assert result.exit_code == 0


def test_directory() -> None:
    runner = CliRunner()
    result = runner.invoke(directory)
    assert result.exit_code == 0


def test_print(tmp_profile: str) -> None:
    runner = CliRunner()
    result = runner.invoke(print_profile, [tmp_profile])
    assert result.exit_code == 0


def test_print_dict(tmp_profile: str, tmp_settings_dict: dict[str, str]) -> None:
    runner = CliRunner()
    result = runner.invoke(print_profile, [tmp_profile, '--dict'])
    assert result.exit_code == 0
    assert result.output.strip() == f'{tmp_settings_dict}'


def test_add_delete(tmp_config: Path) -> None:
    runner = CliRunner()
    name = 'test-hex-profile-cli'
    result = runner.invoke(add, [str(tmp_config), '--name', name, '--overwrite'])
    assert result.exit_code == 0

    spm = SlurmProfileManager()
    profile = spm.get_profile(name)
    assert profile is not None

    result = runner.invoke(delete, [name])
    assert result.exit_code == 0

    with pytest.raises(FileNotFoundError):
        spm.get_profile(name)
