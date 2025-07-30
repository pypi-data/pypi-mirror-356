from pathlib import Path

import pytest

from shephex.experiment import Options


def test_options_creation() -> None:
    options = Options()
    assert options

def test_options_no_args() -> None:
    options = Options()
    assert options.args == []

def test_options_args() -> None:
    options = Options(1, 2, 3)
    assert options.args == [1, 2, 3]

def test_options_args_list() -> None:
    options = Options(1, 2, 3, [4, 5])
    assert options.args == [1, 2, 3, [4, 5]]

def test_options_args_list_invalid() -> None:
    with pytest.raises(TypeError):
        Options(1, 2, 3, [object, 5])

def test_options_args_dict() -> None:
    args = [1, 2, 3, {'a': 1, 'b': 2}]
    options = Options(*args)
    assert options.args == args

def test_options_args_dict_invalid() -> None:
    args = [1, 2, 3, {'a': object, 'b': 2}]
    with pytest.raises(TypeError):
        Options(*args)

def test_options_kwargs() -> None:
    options = Options(a=1, b=2, c=3)
    assert options.kwargs == {'a': 1, 'b': 2, 'c': 3}

def test_options_kwargs_invalid() -> None:
    with pytest.raises(TypeError):
        Options(a=object, b=2, c=3)

def test_options_print() -> None:
    options = Options(a=1, b=2, c=3)
    print(options)

def test_options_dump_path(tmp_path: Path) -> None:
    options = Options(a=1, b=2, c=3)
    options.dump(tmp_path)
    loaded = Options.load(tmp_path)
    assert options == loaded

def test_options_dump_path_str(tmp_path: Path) -> None:
    options = Options(1, 2, 3, a=1, b=2, c=3)
    options.dump(str(tmp_path))
    loaded = Options.load(str(tmp_path))
    assert options == loaded

def test_optioms_to_dict() -> None:
    options = Options(1, 2, 3, a=1, b=2, c=3)
    assert options.to_dict() == {
        'args': [1, 2, 3],
        'a': 1,
        'b': 2,
        'c': 3
    }

def test_options_equals_same() -> None:
    options = Options(1, 2, 3, a=1, b=2, c=3)
    assert options == options

def test_options_equals_different() -> None:
    options = Options(1, 2, 3, a=1, b=2, c=3)
    other = Options(1, 2, 3, a=1, b=2, c=4)
    assert options != other

def test_options_equals_different_args() -> None:
    options = Options(1, 2, 3, a=1, b=2, c=3)
    other = Options(1, 2, 4, a=1, b=2, c=3)
    assert options != other

def test_options_equals_different_type() -> None:
    options = Options(1, 2, 3, a=1, b=2, c=3)
    assert options != object()

def test_options_items() -> None:

    args = [1, 2, 3]
    kwargs = {'a': 1, 'b': 2, 'c': 3}

    options = Options(*args, **kwargs)

    for key, value in options.items():
        if key == 'args':
            assert value == args
        else:
            assert value == kwargs[key]

def test_options_keys() -> None:

    args = [1, 2, 3]
    kwargs = {'a': 1, 'b': 2, 'c': 3}

    options = Options(*args, **kwargs)

    assert options.keys() == list(kwargs.keys()) + ['args']

def test_options_values() -> None:
    args = [1, 2, 3]
    kwargs = {'a': 1, 'b': 2, 'c': 3}

    options = Options(*args, **kwargs)

    for value in options.values():
        correct = value == args or value in kwargs.values()
        assert correct

def test_options_getitem() -> None:
    args = [1, 2, 3]
    kwargs = {'a': 1, 'b': 2, 'c': 3}

    options = Options(*args, **kwargs)

    for key in options.keys():
        if key in kwargs:
            assert options[key] == kwargs[key]
        else:
            options[key] == args