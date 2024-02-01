Initialize Migration
````commandline
alembic init alembic
````

Introduce migration

````commandline
alembic revision --autogenerate -m "[Migration Name]"
````

Update after migration

```commandline
alembic upgrade head
```