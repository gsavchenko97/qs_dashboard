import json
import os


class DataBase:
    DB_FOLDER = '.db'
    AVAILABLE_METRICS = {
        'киллограмм', 'метр', 'грамм'
    }

    def __init__(self, username):
        self.username = username
        self.db_path = f'{os.path.join(self.DB_FOLDER, "database")}.db'
        self.db = self.load_db()
        self.metrics = {}

    def save_db(self):
        assert self.db != {}, 'trying to save empty db'
        json.dump(self.db, open(self.db_path, 'w'))

    def load_db(self):
        if os.path.exists(self.db_path):
            return json.load(open(self.db_path))
        else:
            return {}

    def clean_whole_db(self):
        self.db = {}
        if os.path.exists(self.db_path):
            os.system(f'rm {self.db_path}')

    def clean_user_db(self, username):


    def add_measurement(self, measurement_name, value, metric, day):
        should_convert = False
        from_metric = metric
        if measurement_name in self.metrics and self.metrics[measurement_name] != metric:
            should_convert = True
            from_metric = self.metrics[measurement_name]

        if self.username not in self.db:
            self.db[self.username] = {}
        db = self.db[self.username]

        if measurement_name not in db:
            db[measurement_name] = [value]
            self.metrics[measurement_name] = metric
        else:
            if should_convert:
                db[measurement_name] = self.convert_values(db[measurement_name], from_metric, metric)

    def convert_values(self, db, from_metric, to_matric):
        return db







