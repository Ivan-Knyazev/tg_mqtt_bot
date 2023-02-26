# DataBase Revisions and Migrations


## Initialize alembic migrations

`alembic init migrations`


## Autogenerate Revisions

`alembic revision --autogenerate -m "<message>"`


## Create migrations

`alembic upgrade <revision_hash>`

`alembic downgrade <revision_hash>`