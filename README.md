# DuelGame

Game for UfoPrask Spring 2018.

## Installation

First, best things to do is create virtualenv.

Second, install Python project requirements

```
pip install -r requirements.txt
```

Run Django database migrations and populate DB from `duel_game` directory.

```
python manage.py migrate
python manage.py populate_db
```
Create admin user:

```
python manage.py createsuperuser
```

And finally, run server:

```
python manage.py runserver
```
