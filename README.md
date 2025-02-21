# diplom

## application description

* git, python, venv
* database: sqlite
* backend: django, django-admin

### workspace setup

#### project preparation
```shell
git clone https://www.github.com/jgkarl/diplom 
cd diplom
cp .env.example .env
```

#### python preparation 
  * initialize virtual env
  * install python dependencies within root folder

```shell
python --version
python -m venv .venv 
source .venv/bin/activate

pip install -r requirements.txt

## initial project setup
# python -m pip install Django
python -m django --version
mkdir backend
django-admin startproject core backend
```

#### initialize database and migrate
* default ``db.sqlite3`` database is created automatically
```shell
python backend/manage.py makemigrations 
python backend/manage.py migrate
```

## application
* create django superuser, ``--noinput`` means default ``.env`` values
```shell
python backend/manage.py createsuperuser --noinput
```

### run django server
```shell
python backend/manage.py runserver
```

### default application access
* [client on - localhost:8000](http://127.0.0.1:8000)
* [admin on - localhost:8000/admin](http://127.0.0.1:8000/admin)