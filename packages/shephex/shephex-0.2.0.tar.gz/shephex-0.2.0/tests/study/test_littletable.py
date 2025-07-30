from pathlib import Path
from typing import Callable, List

import pytest

from shephex import Experiment
from shephex.study.table.littletable_table import LittleTable, safe_getattr


@pytest.fixture()
def table(experiments: list) -> LittleTable:
	table = LittleTable()
	for experiment in experiments:
		table.add_row(experiment.to_dict())
	return table


def test_table(table: LittleTable) -> None:
	assert isinstance(table, LittleTable)


def test_table_contains_id(table: LittleTable, experiment_0: Experiment) -> None:
	assert table.contains_row(experiment_0.to_dict()) # Experiment_0 is in the table.
	
def test_table_contains_data(table: LittleTable, experiment_factory: Callable, tmp_path: Path) -> None:
    experiment = experiment_factory(0, 1, tmp_path) # Same settings as experiment_0
    assert table.contains_row(experiment.to_dict())
	
def test_table_not_contains_data(table: LittleTable, experiment_factory: Callable, tmp_path: Path) -> None:
    experiment = experiment_factory(1, 2, tmp_path) # Different settings.
    assert not table.contains_row(experiment.to_dict())

def test_table_get_row_match(table: LittleTable, experiment_0: Experiment) -> None:
    match = table.get_row_match(experiment_0.identifier)
    assert match.identifier == experiment_0.identifier

def test_table_get_row_match_error(table: LittleTable) -> None:
    with pytest.raises(ValueError):
        table.get_row_match('non_existing_identifier')

def test_table_where_1(table: LittleTable, experiment_0: Experiment) -> None:
    match = table.where(identifier=experiment_0.identifier)
    assert len(match) == 1

def test_table_where_2(table: LittleTable, experiments: List[Experiment]) -> None:
    match = table.where(a=1)
    count = 0
    for experiment in experiments:
        if experiment.options.kwargs['a'] == 1:
            count += 1

    assert len(match) == count

def test_table_update_row(table: LittleTable, experiment_0: Experiment) -> None:
    experiment_0.status = 'running'
    table.update_row(experiment_0.to_dict())
    match = table.get_row_match(experiment_0.identifier)
    assert match.status == 'running'

def test_table_update_row_partially(table: LittleTable, experiment_0: Experiment) -> None:
    experiment_dict = experiment_0.to_dict()
    experiment_dict.pop('status')
    table.update_row_partially(experiment_dict)
    match = table.get_row_match(experiment_0.identifier)
    assert match.status == experiment_0.status
	
def test_safe_getattr(experiment_0: Experiment) -> None:
    assert safe_getattr(experiment_0, 'identifier') == experiment_0.identifier
    assert safe_getattr(experiment_0, 'non_existing_key') is None
    

	


