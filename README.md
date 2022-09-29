1) POSTGRES DEMO DATABASE is required to be loaded in the Postgres (named 'demo')

https://postgrespro.ru/docs/postgrespro/10/demodb-bookings-installation.html

2) LAUNCH PROJECT:

```
flask run -p 8005 --cert=certs/localhost.crt --key=certs/localhost.key
```

3) YOU CAN VIEW ALL ROUTES:

```
flask routes
```

4) RUNNING TESTS:

```
python -m pytest -vv
```

