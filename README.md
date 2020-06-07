# QuantifiedSelf Dashboard

Программа, позволяющяя строить графики по пользовательским данным.

Например, можно добавлять данные о весе, результатах замеров давления, измерениях содержания сахара в крови,
денежных расходах и т.п. Возможность строить графики прогресса по дням.
Программа многопользовательская, для испольования необходимо зарегистрировать личный аккаунт.
Для каждого пользователя хранится отдельная "база данных".

В приложении можно смотреть графики, выбирать для них единицы измерения, добавлять измерение очередного дня,
сохранять данные в файл, загружать данные из файла.

# Эскиз интерфейса:
Графический интерфейс приложения выглядит следующим образом:

![Эскиз интерфейса](https://github.com/gsavchenko97/qs_dashboard/blob/master/qs_dashboard_gui.png)


# Установка:
Установить программу можно разными способами:
+ строим whl файл и устанавливаем его запускаем
```bash
git clone https://github.com/gsavchenko97/qs_dashboard.git
cd qs_dashboard
make wheel

. venv/bin/activate
pip install dist/*.whl
qs_dashboard # запуск программы
deactivate

```

+ запуск с репозитория
```bash
git clone https://github.com/gsavchenko97/qs_dashboard.git
cd qs_dashboard
make run # запуск программы
```

+ построить бинарник
```bash
git clone https://github.com/gsavchenko97/qs_dashboard.git
cd qs_dashboard
make build
dist/qs_dasboard # запуск программы
```

# Возможности:
+ Графический интерфейс
+ Поддержка русского и анлийского языков
+ возможность запускать тесты через ```make run-tests```
+ возможность проверки на соответствие PEP ```make flake```
+ возможность генерить документацию ```make doc```
+ возможность удалять генераты ```make clean```

# Участники:
Давлетов Адис (524)

Шелудько Борис (524)
