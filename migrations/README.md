# DataBase Revisions and Migrations


## Initialize alembic migrations

`alembic init migrations`


## Autogenerate Revisions

`alembic revision --autogenerate -m "<message>"`


## Create migrations

`alembic upgrade <revision_hash>`

`alembic downgrade <revision_hash>`

### *Show that the current state of the database represents the application of all migrations

`alembic stamp head`