# development setup description

* windows 11, wsl 2, ubuntu 22.04
* python 3.10.12, venv, pip
* database: postgres 14.15
* backend: django 5.1.6, django-admin

## workspace setup
### environment preparation
```shell
sudo apt-get install postgresql postgresql-contrib
```

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

# `deactivate` for deactivation
source .venv/bin/activate

pip install -r requirements.txt

## initial project setup
# python -m pip install Django
python -m django --version
mkdir backend
django-admin startproject core backend
```

#### database setup
* initial ``db.sqlite3`` database is created automatically
* initial postgres is configured via ``.env`` variable values

```shell
psql postgres
```

```sql
DROP database diplom with (force);

CREATE ROLE diplom_admin WITH LOGIN CREATEDB CREATEROLE PASSWORD 'diplom_password';
ALTER ROLE diplom_admin SET client_encoding TO 'utf8';
ALTER ROLE diplom_admin SET default_transaction_isolation TO 'read committed';
ALTER ROLE diplom_admin SET timezone TO 'Europe/Tallinn';
CREATE ROLE diplom_manager WITH LOGIN;
ALTER ROLE diplom_manager SET client_encoding TO 'utf8';
ALTER ROLE diplom_manager SET default_transaction_isolation TO 'read committed';
ALTER ROLE diplom_manager SET timezone TO 'Europe/Tallinn';

DROP DATABASE IF EXISTS diplom WITH (FORCE);
CREATE DATABASE diplom WITH ENCODING 'UTF8' TEMPLATE=template0;

GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA public TO diplom_manager;
ALTER DEFAULT PRIVILEGES GRANT SELECT, INSERT, UPDATE ON TABLES TO diplom_manager;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO diplom_manager;
ALTER DEFAULT PRIVILEGES GRANT USAGE, SELECT ON SEQUENCES TO diplom_manager;
REVOKE GRANT OPTION FOR ALL PRIVILEGES ON ALL TABLES IN SCHEMA public FROM diplom_manager;
ALTER DEFAULT PRIVILEGES REVOKE GRANT OPTION FOR ALL PRIVILEGES ON TABLES FROM diplom_manager;

REVOKE CREATE ON SCHEMA public FROM PUBLIC;
GRANT CREATE ON SCHEMA public TO diplom_admin;
ALTER DATABASE diplom OWNER TO diplom_admin;
```

```shell
psql -d postgresql://diplom_admin:diplom_password@localhost:5432/diplom
```

#### migrate database
```shell
python backend/manage.py makemigrations 
python backend/manage.py migrate
python backend/manage.py createsuperuser --noinput
```


### prepare backend (django) and frontend (vue)
```shell
# install all node packages - includes backend/theme/static_src/package.json
npm install 
# starts `vite` server that delivers VueJS `frontend` application
npm run dev
npm run build
# hot reload for django theme tailwindcss
python backend/manage.py tailwind build
python backend/manage.py tailwind start
```

### run django server
```shell
python backend/manage.py makemessages -l en
python backend/manage.py makemessages -l et
python backend/manage.py compilemessages

python backend/manage.py collectstatic --no-input

python backend/manage.py runserver
```

### default application access
* [django frontend - localhost:8000](http://127.0.0.1:8000)
* [django-admin - localhost:8000/admin](http://127.0.0.1:8000/admin)
* [django book - localhost:8000/book/list](http://127.0.0.1:8000/book/list)
* [vue-vite book - localhost:8000/book](http://127.0.0.1:8000/book)


### helpers

* clean up temporary migrations
`find . -type d -name "migration*" -not -path "./.venv/*" -exec find {} -type f -name "*.py" ! -name "__init__.py" -delete \;`
