import pytest

from shephex.executor.slurm import SlurmHeader, valid_options


def test_slurm_header() -> None:
    SlurmHeader()

@pytest.mark.parametrize('key', [option[1] for option in valid_options[0:10]])
def test_slurm_add_option_long(key: str) -> None:
    header = SlurmHeader()
    header.add(key.replace('--', ''), 'value')

@pytest.mark.parametrize('key', [option[0] for option in valid_options if option[0] is not None])
def test_slurm_add_option_short(key: str) -> None:
    header = SlurmHeader()
    header.add(key.replace('-', ''), 'value')

def test_slurm_add_option_invalid() -> None:
    header = SlurmHeader()
    with pytest.raises(ValueError):
        header.add('invalid', 'value')

def test_slurm_header_repr() -> None:
    header = SlurmHeader()
    header.add('partition', 'gpu')
    assert repr(header).splitlines()[1] == '#SBATCH --partition=gpu'

def test_slurm_header_str() -> None:
    header = SlurmHeader()
    header.add('partition', 'gpu')
    assert str(header).splitlines()[1] == '#SBATCH --partition=gpu'

def test_slurm_header_add_duplicate() -> None:
    header = SlurmHeader()
    header.add('partition', 'gpu')
    with pytest.raises(ValueError):
        header.add('partition', 'gpu')

def test_slurm_header_copy() -> None:
    header = SlurmHeader()
    header.add('partition', 'gpu')
    header_copy = header.copy()
    assert str(header) == str(header_copy)
    assert header is not header_copy
