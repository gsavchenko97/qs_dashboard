"""
high level support for data storing and manipulations
=====================================================
lorem ipsum lorem ipsum lorem ipsum lorem ipsum
lorem ipsum lorem ipsum lorem ipsum lorem ipsum
lorem ipsum lorem ipsum
lorem ipsum lorem ipsum lorem ipsum lorem ipsum
"""

import json
import os
from pathlib import Path
import pandas as pd
from dashboard.utils.user import DB_FOLDER, AVAILABLE_METRICS
from typing import Dict


def not_empty_db(db: Dict[str, list]) -> bool:
    """
    Checks if db is empty
    :type db: Dict
    :param db: database to check
    :return: True or False
    """
    return len(db) > 0 and len(list(db.values())[0])


def get_scaled_to_range(values, start_range, end_range):
    """
    Returns list of values scaled to range from start_range to end_range
    :param values: list of values to scale
    :param start_range: start of the scaling range
    :param end_range: end of the scaling range
    :return: scaled list of values
    """
    minimum = min(values)
    maximum = max(values)
    values = [(value - minimum) / (maximum - minimum) for value in values]  # scaling to [0, 1]
    values = [(end_range - start_range) * value for value in values]  # scaling to [0, end_range - start_range]
    values = [value + start_range for value in values]  # scaling to [start_range, end_range]
    return values


class DataBase:
    """
    DataBase class which stores all the information about users and their
    daily measurement results. It could save current state of the database and load database from
    existing dump. All the information stored in dictionary of dictionaries. For every user we have
    a dictionary mapping some measurement result and day in which it was performed to measurement name.
    """
    DB_FOLDER = str(Path(__file__).resolve().parent.parent / ".db")
    AVAILABLE_METRICS = {
        'kg', 'gr',
        'mg', 'ton',
        'km', 'm',
        'cm', 'mm',
        'km ** 2', 'm ** 2',
        'cm ** 2', 'mm ** 2',
        'hour', 'minute', 's', 'ms',
        'km ** 3', 'm ** 3',
        'cm ** 3', 'mm ** 3', 'liter',
        'ruble', 'dollar',
        'euro'
        }

    def __init__(self, username, load_from_saved=True):
        """
        DataBase object initialization
        :param username: user's name
        """
        self.DB_FOLDER = DB_FOLDER
        self.AVAILABLE_METRICS = AVAILABLE_METRICS
        if not os.path.exists(DB_FOLDER):
            os.makedirs(DB_FOLDER, exist_ok=True)
        self.username = username
        self.db_path = os.path.join(self.DB_FOLDER, f"database-{username}.json")
        self.metrics_converter_path = os.path.join(self.DB_FOLDER, f"metrics_converter-{username}.json")
        if load_from_saved:
            self.db = self.load_db(self.db_path)
            self.metrics_converter = self.load_metrics_converter(self.metrics_converter_path)
        else:
            self.db = {}
            self.metrics_converter = {}
        self.metrics = {}

    def set_db(self, db):
        self.db = db

    def set_metrics(self, metrics):
        self.metrics = metrics

    def save_db(self, path):
        """
        saves database state
        :return: None
        """
        assert not_empty_db(self.db), 'trying to save empty db'
        json.dump(self.db, open(path, 'w'))

    def load_db(self, path):
        """
        loads database from dump
        :return: database from DataBase class
        """
        if os.path.exists(path):
            result = json.load(open(path))
        else:
            result = {}
        return result

    def save_to_dataframe(self, path):
        """
        saves database in csv file
        :param path: path to save
        :return: None
        """
        df = self.to_dataframe()
        df.to_csv(path, index=False)

    def load_from_df(self, path):
        df = pd.read_csv(path)
        db, metrics = self.from_dataframe(df, self_init=False)
        return db, metrics

    def load_metrics_converter(self, path):
        """
        loads saved converter for metrics
        :return: None
        """
        if os.path.exists(path):
            from_saved = json.load(open(path))
            metrics_converter = {}
            for key in from_saved:
                metrics_converter[tuple(key.split('+'))] = from_saved[key]
            result = metrics_converter
        else:
            result = {}
        return result

    def save_metrics_converter(self, path):
        """
        saves metrics_converter for metrics from DataBase class
        :return: None
        """
        assert self.metrics_converter != {}, 'trying to save empty metrics converter'
        to_save = {}
        for key in self.metrics_converter:
            to_save['+'.join(key)] = self.metrics_converter[key]
        json.dump(to_save, open(path, 'w'))

    def add_metrics_convertion(self, from_metric, to_metric, from_value, to_value):
        """
        adds metrics convert rule to metrics_converter from DataBase class
        :param from_metric: one of the metrics from convert rule
        :param to_metric: one of the metrics from convert rule
        :param from_value: value for one of the metrics
        :param to_value: corresponding value of the second metric
        :return: None
        """
        assert from_metric in self.AVAILABLE_METRICS
        assert to_metric in self.AVAILABLE_METRICS
        self.metrics_converter[(from_metric, to_metric)] = to_value / from_value
        self.metrics_converter[(to_metric, from_metric)] = from_value / to_value
        self.save_metrics_converter(self.metrics_converter_path)

    def clean_whole_db(self):
        """
        removes saved dump of the database
        :return: None
        """
        self.db = {}
        self.metrics_converter = {}
        self.metrics = {}
        if os.path.exists(self.db_path):
            os.system(f'rm {self.db_path}')
            os.system(f'rm {self.metrics_converter_path}')

    def if_metric_convertation_need(
        self,
        measurement_name,
        metric
    ):
        """
        check if there is the need to update values of
        measurement with respect to new metric
        :param measurement_name: measurement name that is needed to be added
        :param metric: metric in which value is needed to be added
        :return: tuple of bool, and last metric for measurement
        """
        should_convert = False
        from_metric = metric
        if measurement_name in self.metrics and self.metrics[measurement_name] != metric:
            should_convert = True
            from_metric = self.metrics[measurement_name]

        return should_convert, from_metric

    def add_measurement(
            self,
            measurement_name: str,
            value: float,
            metric: str,
            day: int):
        """
        adds measurement result to database
        :param measurement_name: measurement naming
        :param value: value of measurement
        :param metric: metric of the value
        :param day: day in which measurement was done
        :return: None
        """
        assert value >= 0, 'trying to add negative value'

        successfully_converted = True

        should_convert, from_metric = self.if_metric_convertation_need(
            measurement_name,
            metric)

        db = self.db

        if measurement_name not in db:
            db[measurement_name] = []
            db[f'{measurement_name}_days'] = []

        if should_convert:
            try:
                db[measurement_name] = self.convert_values(
                    db[measurement_name],
                    from_metric,
                    to_metric=metric
                )
            except ValueError:
                successfully_converted = False

        if successfully_converted:
            assert len(db[f'{measurement_name}_days']) == 0 or \
                   day > db[f'{measurement_name}_days'][-1], 'trying to add the day ' \
                                                             'prior or equal to last added'
            db[measurement_name].append(value)
            db[f'{measurement_name}_days'].append(day)
            self.metrics[measurement_name] = metric

        self.db = db

    def convert_values(self, values, from_metric, to_metric):
        """
        converts values according convert rules from metrics_converter from DataBase class
        :param values: values to convert
        :param from_metric: convert from metric
        :param to_metric: convert to metric
        :return:
        """
        multiply_factor = self.metrics_converter[(from_metric, to_metric)]
        values = [value * multiply_factor for value in values]
        return values

    def to_dataframe(self, default_value=-1):
        """
        converts database and metrics from DataBase class to pandas DataFrame
        :param default_value: value to fill for missing measures
        :return: pandas DataFrame constructed from database and metrics
        """
        if len(self.db) == 0:
            return pd.DataFrame()
        db = self.db
        metrics = self.metrics
        df = {
            'measurement_name': [],
            'value': [],
            'metric': [],
            'day': []
        }
        minimal_day = min(
            [day for key, days in db.items() for day in days if
                '_days' in key]
        )

        maximal_day = max(
            [day for key, days in db.items() for day in days if
                '_days' in key]
        )

        for measurement_name in sorted(db.keys()):
            if '_days' in measurement_name:
                continue
            days = db[f'{measurement_name}_days']
            for day in range(minimal_day, maximal_day + 1):
                value = default_value
                if day in days:
                    value = db[measurement_name][
                        db[f'{measurement_name}_days'
                    ].index(day)]

                df['measurement_name'].append(measurement_name)
                df['value'].append(value)
                df['metric'].append(metrics[measurement_name])
                df['day'].append(day)

        return pd.DataFrame(df)

    def from_dataframe(
            self,
            dataframe: pd.DataFrame,
            default_value: float = -1.0,
            self_init: bool = True):
        """
        reverse to self.to_dataframe(database, metrics, default_value=-1)
        converts pandas DataFrame in appropriate format to database and metrics in DataBase class
        :param self_init: whether to init self object
        :param dataframe: pandas DataFrame to convert
        :param default_value: value denoting missing values in csv
        :return: None
        """
        df = dataframe.copy()
        db = {}

        metrics = dict(
            df.apply(lambda r: (r.measurement_name, r.metric), axis=1).unique()
        )

        total_measurements = df.measurement_name.unique()
        for measurement_name in total_measurements:
            measurement_df = df[df.measurement_name == measurement_name]
            indices = [
                i for i, value in enumerate(measurement_df.value.values) if
                    value != default_value
            ]
            days = [
                day for i, day in enumerate(measurement_df.day.values) if
                    i in indices
            ]
            values = [
                value for i, value in enumerate(measurement_df.value.values) if
                    i in indices
            ]
            db[measurement_name] = [float(value) for value in values]
            db[f'{measurement_name}_days'] = [int(day) for day in days]

        if self_init:
            self.db = db
            self.metrics = metrics

        return db, metrics
