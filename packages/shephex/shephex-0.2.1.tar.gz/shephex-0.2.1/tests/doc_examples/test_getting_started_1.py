# ruff: noqa
import shephex
from typing import ContextManager
import pytest

# --8<-- [start:part1]    
@shephex.chain()
def my_function(a, b, c):
    return a + b + c
# --8<-- [end:part1]

def code_example() -> None:
    # --8<-- [start:func]
    # --8<-- [start:part2]
    experiments = (
        my_function(directory='experiments')
        .zip(a=[1, 2], b=[4, 5])
        .permute(c=[7, 8, 9])
        )
    # --8<-- [end:part2]

    # --8<-- [start:part3]
    executor = shephex.executor.LocalExecutor()
    executor.execute(experiments)
    # --8<-- [end:part3]
    # --8<-- [end:func]

def code_example_2() -> None:
    import shephex

    # --8<-- [start:load]
    results, options = shephex.result_where(a=1, b=4, directory='experiments')

    for result, option in zip(results, options):
        print(option.kwargs, result)
    # --8<-- [end:load]
    assert len(results) == 3
    assert len(options) == 3


def test_code_example(tmpdir_context_manager: ContextManager) -> None:
    try:
        with tmpdir_context_manager:
            code_example()
            code_example_2()
    except Exception as e:
        pytest.fail(f"Error: {e}")