import json
import os


def not_empty_db(db):
    if any([len(x) > 0 for x in db.values()]):
        return True
    else:
        return False


def get_scaled_to_range(values, a, b):
    minimum = min(values)
    maximum = max(values)
    values = [(value - minimum) / (maximum - minimum) for value in values]  # scaling to [0, 1]
    values = [(b - a) * value for value in values]  # scaling to [0, b - a]
    values = [value + a for value in values]  # scaling to [a, b]
    return values


class DataBase:
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
        'мм ** 3', 'литр'
    }

    def __init__(self, username):
        self.username = username
        self.db_path = os.path.join(self.DB_FOLDER, "database.json")
        self.metrics_converter_path = os.path.join(self.DB_FOLDER, 'metrics_converter.json')
        self.db = self.load_db()
        self.metrics_converter = self.load_metrics_converter()
        self.metrics = {}

    def save_db(self):
        assert not_empty_db(self.db), 'trying to save empty db'
        json.dump(self.db, open(self.db_path, 'w'))

    def load_db(self):
        if os.path.exists(self.db_path):
            return json.load(open(self.db_path))
        else:
            return {}

    def load_metrics_converter(self):
        if os.path.exists(self.metrics_converter_path):
            return json.load(open(self.metrics_converter_path))
        else:
            return {}

    def save_metrics_converter(self):
        assert self.metrics_converter != {}, 'trying to save empty metrics converter'
        json.dump(self.metrics_converter, open(self.metrics_converter_path, 'w'))

    def add_metrics_convertion(self, from_metric, to_metric, from_value, to_value):
        assert from_metric in self.AVAILABLE_METRICS
        assert to_metric in self.AVAILABLE_METRICS
        self.metrics_converter[(from_metric, to_metric)] = to_value / from_value
        self.metrics_converter[(to_value, from_value)] = from_value / to_value
        self.save_metrics_converter()

    def clean_whole_db(self):
        self.db = {}
        if os.path.exists(self.db_path):
            os.system(f'rm {self.db_path}')

    def clean_user_db(self):
        self.db[self.username] = {}
        self.save_db()

    def add_measurement(self, measurement_name, value, metric, day):
        should_convert = False
        from_metric = metric
        successfully_added = True
        if measurement_name in self.metrics and self.metrics[measurement_name] != metric:
            should_convert = True
            from_metric = self.metrics[measurement_name]

        if self.username not in self.db:
            self.db[self.username] = {}
        db = self.db[self.username]

        if measurement_name not in db:
            db[measurement_name] = [value]
            db[f'{measurement_name}_{day}'] = [day]
        else:
            if should_convert:
                try:
                    db[measurement_name] = self.convert_values(db[measurement_name], from_metric, to_metric=metric)
                except ValueError:
                    successfully_added = False
            if successfully_added:
                db[measurement_name].append(value)
                db[f'{measurement_name}_{day}'].append(day)

        self.metrics[measurement_name] = metric
        self.db[self.username] = db

    def convert_values(self, values, from_metric, to_metric):
        multiply_factor = self.metrics_converter[(from_metric, to_metric)]
        values = [value * multiply_factor for value in values]
        return values
