# Nginx Logs
## Description

Saves logs from url or file to database

## Requirements

- Docker Compose
- Python 3.12

## Installing

Clone project and create .env file:

```bash
POSTGRES_USERNAME=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=db
POSTGRES_PORT=5432
POSTGRES_NAME=postgres
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@example.com
DJANGO_SUPERUSER_PASSWORD=admin
SECRET_KEY='django-insecure-q@(%$l+n)6z^f7cby&q(=6oak_a(lyiib)og6j-mfns(dga1^o'
```

## Run

Open terminal and run command:

   ```bash
   docker-compose up --build
   ```

## Fill database

Open terminal and run command:

   ```bash
   docker-compose run app python manage.py import_ngix_log log_url
   ```
log_url could be url or path to local file

## Tests

Open terminal and run command:

   ```bash
   docker-compose run app python manage.py test
   ```

## Api

```
admin/
api/
swagger/
swagger.json/
swagger.yaml/
```
