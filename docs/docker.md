# docker project description

* windows 11, wsl 2, ubuntu 22.04, vs-code
* docker desktop, docker compose

### workspace setup

## initialize docker project from git repository root folder
* ``docker-compose.yml`` via ``.env``

```shell
docker compose up -d
```

## backend application initialization within backend container
```shell
# creates model migrations based on python models declarations
docker compose exec backend python manage.py makemigrations
# migrates main database based on previous files created
docker compose exec backend python manage.py migrate
# creates new djagno superuser (--noinput credentials via .env)
docker compose exec backend python manage.py createsuperuser --noinput

# i18n translation plugin creates messages that are queried via translation function
docker compose exec backend python manage.py makemessages -l en
docker compose exec backend python manage.py makemessages -l et
# i18n compiles files into .po binary translations files
docker compose exec backend python manage.py compilemessages

# backend/theme app customizes templates while using tailwind 
# `python manage.py tailwind start` should be used while developing
docker compose exec backend python manage.py tailwind build

# collects static files from applications, incl. frontend Vue-Vite js files
docker compose exec backend python manage.py collectstatic --no-input

# database migrations for base Book module
docker compose exec backend sh /app/scripts/book_import.sh

# database migrations for tagging module
docker compose exec backend sh /app/scripts/tag_import.sh

```