# Diplomitööde rakendus

## application description

* Django (python) backend, django-admin
* Vue (vite) frontend applets
* Postgres for backend main database
* Neo4j for graph database and network analysis and visual

## Workspace

### Setup and Configurations

* Important variables within `.env` file
* [Localized setup](./docs/setup.md)
* [Docker configuration](./docs/docker.md)

* Django `backend/core/settings.py` has main configurations
* Python scripts are executed with `python backend/manage.py <command>`

* Initial ``db.sqlite3`` database is Djangos default
* Initial postgres is configured via ``.env`` variable values and `database/init.sql` script

### Accessing application

* [Django Frontend - localhost:8000](http://127.0.0.1:8000)
* [Django Admin Module - localhost:8000/admin](http://127.0.0.1:8000/admin)
* [Django Custom Book module - localhost:8000/book/list](http://127.0.0.1:8000/book/list)
* [Vue Vite flavoured applet - localhost:8000/book](http://127.0.0.1:8000/book)