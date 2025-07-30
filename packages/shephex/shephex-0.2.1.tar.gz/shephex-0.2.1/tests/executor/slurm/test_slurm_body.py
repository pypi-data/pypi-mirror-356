import pytest

from shephex.executor.slurm import SlurmBody


def test_slurm_body() -> None:
    SlurmBody()

def test_slurm_body_add() -> None:
    body = SlurmBody()
    body.add('echo "Hello World!"')

def test_slurm_body_add_invalid() -> None:
    body = SlurmBody()
    with pytest.raises(TypeError):
        body.add(1)

def test_slurm_body_add_list() -> None:
    body = SlurmBody()
    body.add(['echo "Hello World!"', 'echo "Goodbye World!"'])

def test_slurm_body_add_list_invalid() -> None:
    body = SlurmBody()
    with pytest.raises(TypeError):
        body.add([1, 2, 3])

def test_slurm_body_repr() -> None:
    body = SlurmBody()
    body.add('echo "Hello World!"')
    assert repr(body) == 'echo "Hello World!"'

def test_slurm_body_str() -> None:
    body = SlurmBody()
    body.add('echo "Hello World!"')
    assert str(body) == 'echo "Hello World!"'

def test_slurm_body_commands_init() -> None:
    commands = ['echo "Hello World!"', 'echo "Goodbye World!"']
    body = SlurmBody(commands)

    body_two = SlurmBody()
    body_two.add(commands)

    assert str(body) == str(body_two)

def test_slurm_body_add_bodies() -> None:
    body = SlurmBody()
    body.add('echo "Hello World!"')
    
    body_two = SlurmBody()
    body_two.add('echo "Hello World!"')

    body = body + body_two
    assert str(body) == 'echo "Hello World!"\necho "Hello World!"'


