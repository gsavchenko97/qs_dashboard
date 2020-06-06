import pytest
import pandas as pd

from dashboard.db import *


@pytest.fixture
def empty_db():
    return {}


@pytest.fixture
def non_empty_db():
    return {'user_x': {'measure_y': [1, 2, 3]}}


@pytest.fixture
def database():
    database = DataBase('user_x', False)

    database.add_measurement('measurement_x', 1, 'gr', 1)
    database.add_measurement('measurement_y', 4, 'kg', 1)
    database.add_metrics_convertion('gr', 'kg', 1000, 1)
    database.add_measurement('measurement_x', 0.002, 'kg', 2)
    database.add_measurement('measurement_y', 3, 'kg', 2)

    return database


@pytest.fixture
def metrics():
    return {
        'measurement_x': 'kg',
        'measurement_y': 'kg'
        }


csv = {
    'username': ['user_x'] * 4,
    'measurement_name': ['measurement_x'] * 2 + ['measurement_y'] * 2,
    'value': [0.001, 0.002, 4, 3],
    'metric': ['kg'] * 4,
    'day': [1, 2, 1, 2]
    }


@pytest.fixture
def csv_data_frame():
    return pd.DataFrame(csv)


def test_not_empty_db(empty_db, non_empty_db):
    result = not_empty_db(empty_db)
    assert not result, 'empty_db is not empty'
    result = not_empty_db(non_empty_db)
    assert result, 'non_empty_db is empty'


def test_get_scaled_to_range():
    values = [0, 1, 2, 3, 4]
    reference = [x / 4 for x in values]
    result = get_scaled_to_range(values, 0, 1)
    assert result == reference, 'values scaled to [0, 1] the wrong way'


def test_convert_db_and_metrics_to_csv(database):
    result = convert_db_and_metrics_to_csv(database.db, database.metrics)
    df = pd.DataFrame(csv)
    print(df)
    print(result)
    assert list(result['username']) == list(df['username'])
    assert list(result['measurement_name']) == list(df['measurement_name'])
    assert list(result['value']) == list(df['value'])
    assert list(result['metric']) == list(df['metric'])
    assert list(result['day']) == list(df['day'])


def test_convert_csv_to_db_and_metrics(csv_data_frame, metrics):
    result_db, result_metrics = \
        convert_csv_to_db_and_metrics(csv_data_frame)
    reference_db = {
        'user_x': {
            'measurement_x': [0.001, 0.002],
            'measurement_x_days': [1, 2],
            'measurement_y': [4, 3],
            'measurement_y_days': [1, 2],
            }
        }
    print(result_db)
    print(reference_db)
    print(result_metrics)
    print(metrics)
    assert result_db == reference_db
    assert result_metrics == metrics


def test_metrics_convertion(database):
    from_metric = 'gr'
    to_metric = 'kg'
    from_values = [1, 2, 3, 4, 6]
    to_values = [x / 1000 for x in from_values]
    result = database.convert_values(
        values=from_values,
        from_metric=from_metric,
        to_metric=to_metric
        )

    assert result == to_values

    result = database.convert_values(
        values=to_values,
        from_metric=to_metric,
        to_metric=from_metric
        )

    assert result == from_values
