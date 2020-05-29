"""
high level support for data storing
"""

import json
import os
import pandas as pd


def not_empty_db(db):
    """
    Checks if db is empty
    :param db: database to check
    :return: True or False
    """
    return any([len(x) > 0 for x in db.values()])


def get_scaled_to_range(values, a, b):
    """
    Returns list of values scaled to range from a to b
    :param values: list of values to scale
    :param a: start of the scaling range
    :param b: end of the scaling range
    :return: scaled list of values
    """
    minimum = min(values)
    maximum = max(values)
    values = [(value - minimum) / (maximum - minimum) for value in values]  # scaling to [0, 1]
    values = [(b - a) * value for value in values]  # scaling to [0, b - a]
    values = [value + a for value in values]  # scaling to [a, b]
    return values


def convert_db_and_metrics_to_csv(database, metrics, default_value=-1):
    """
    converts database and metrics from DataBase class to pandas DataFrame
    :param database: database from DataBase class
    :param metrics: metrics from DataBase class
    :param default_value: value to fill for missing measures
    :return: pandas DataFrame constructed from database and metrics
    """
    df = {
        'username': [],
        'measurement_name': [],
        'value': [],
        'metric': [],
        'day': []
    }
    minimal_day = min(
        [day for db in database.values() for key, days in db.items() for day in days if '_days' in key])
    maximal_day = max(
        [day for db in database.values() for key, days in db.items() for day in days if '_days' in key])
    for username in database:
        db = database[username]
        for measurement_name in db:
            if '_days' in measurement_name:
                continue
            days = db[f'{measurement_name}_days']
            for day in range(minimal_day, maximal_day + 1):
                value = default_value
                if day in days:
                    value = db[measurement_name][db[f'{measurement_name}_days'].index(day)]

                df['username'].append(username)
                df['measurement_name'].append(measurement_name)
                df['value'].append(value)
                df['metric'].append(metrics[measurement_name])
                df['day'].append(day)

    df = pd.DataFrame(df)

    return df


def convert_csv_to_db_and_metrics(csv, default_value=-1):
    """
    reverse to convert_db_and_metrics_to_csv(database, metrics, default_value=-1)
    converts pandas DataFrame in appropriate format to database and metrics in DataBase class
    :param csv: pandas DataFrame to convert
    :param default_value: value denoting missing values in csv
    :return: tuple of metrics and database from DataBase class
    """
    df = csv.copy()
    db = {}
    metrics = {}
    for username in df.username.unique():
        db[username] = {}
        user_df = df[df.username == username].copy()
        for measurement_name in user_df.measurement_name.unique():
            user_measurement_df = user_df[user_df.measurement_name == measurement_name]
            indices = [i for i, value in enumerate(user_measurement_df.value.values) if value != default_value]
            days = [day for i, day in enumerate(user_measurement_df.day.values) if i in indices]
            values = [value for i, value in enumerate(user_measurement_df.value.values) if i in indices]
            db[username][measurement_name] = values
            db[username][f'{measurement_name}_days'] = days
            metrics[measurement_name] = user_measurement_df.metric.values[0]

    return metrics, db


class DataBase:
    """
    DataBase class which stores all the information about users and their
    daily measurement results. It could save current state of the database and load database from
    existing dump. All the information stored in dictionary of dictionaries. For every user we have
    a dictionary mapping some measurement result and day in which it was performed to measurement name.
    """
    DB_FOLDER = '.db'
    AVAILABLE_METRICS = {
        'киллограмм', 'грамм',
        'миллиграмм',
        'тонна', 'центнер',
        'километр', 'метр', 'дециметр',
        'сантиметр', 'миллиметр',
        'км ** 2', 'м ** 2',
        'гектар', 'дм ** 2',
        'акр', 'см ** 2',
        'мм ** 2', 'час',
        'минута', 'секунда', 'миллисекунда',
        'км ** 3', 'м ** 3',
        'дм ** 3', 'см ** 3',
        'мм ** 3', 'литр',
        'рубль', 'доллар',
        'евро'
    }

    def __init__(self, username):
        """
        DataBase object initialization
        :param username: user's name
        """
        self.username = username
        self.db_path = os.path.join(self.DB_FOLDER, "database.json")
        self.metrics_converter_path = os.path.join(self.DB_FOLDER, 'metrics_converter.json')
        self.db = self.load_db()
        self.metrics_converter = self.load_metrics_converter()
        self.metrics = {}

    def save_db(self):
        """
        saves database state
        :return: None
        """
        assert not_empty_db(self.db), 'trying to save empty db'
        json.dump(self.db, open(self.db_path, 'w'))

    def load_db(self):
        """
        loads database from dump
        :return: database from DataBase class
        """
        if os.path.exists(self.db_path):
            return json.load(open(self.db_path))
        return {}

    def load_metrics_converter(self):
        """
        loads saved converter for metrics
        :return: metrics_converter from DataBase class
        """
        if os.path.exists(self.metrics_converter_path):
            return json.load(open(self.metrics_converter_path))
        return {}

    def save_metrics_converter(self):
        """
        saves metrics_converter for metrics from DataBase class
        :return: None
        """
        assert self.metrics_converter != {}, 'trying to save empty metrics converter'
        json.dump(self.metrics_converter, open(self.metrics_converter_path, 'w'))

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
        self.metrics_converter[(to_value, from_value)] = from_value / to_value
        self.save_metrics_converter()

    def clean_whole_db(self):
        """
        removes saved dump of the database
        :return: None
        """
        self.db = {}
        if os.path.exists(self.db_path):
            os.system(f'rm {self.db_path}')

    def clean_user_db(self):
        """
        removes current user related information from database
        :return: None
        """
        self.db[self.username] = {}
        self.save_db()

    def add_measurement(self, measurement_name, value, metric, day):
        """
        adds measurement result to database
        :param measurement_name: measurement naming
        :param value: value of measurement
        :param metric: metric of the value
        :param day: day in which measurement was done
        :return: None
        """
        assert value >= 0, 'trying to add negative value'
        should_convert = False
        from_metric = metric
        successfully_converted = True
        if measurement_name in self.metrics and self.metrics[measurement_name] != metric:
            should_convert = True
            from_metric = self.metrics[measurement_name]

        if self.username not in self.db:
            self.db[self.username] = {}
        db = self.db[self.username]

        if measurement_name not in db:
            db[measurement_name] = []
            db[f'{measurement_name}_days'] = []

        if should_convert:
            try:
                for username in self.db:
                    if username == self.username:
                        db[measurement_name] = self.convert_values(
                            db[measurement_name],
                            from_metric,
                            to_metric=metric)
                    elif measurement_name in self.db[username]:
                        self.db[username][measurement_name] = self.convert_values(
                            self.db[username][measurement_name],
                            from_metric,
                            to_metric=metric)
                    else:
                        pass
            except ValueError:
                successfully_converted = False

        if successfully_converted:
            assert day > db[f'{measurement_name}_days'][-1], 'trying to add the day ' \
                                                             'prior or equal to last added'
            db[measurement_name].append(value)
            db[f'{measurement_name}_days'].append(day)
            self.metrics[measurement_name] = metric

        self.db[self.username] = db

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
