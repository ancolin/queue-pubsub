#!/bin/ash

/usr/local/bin/uwsgi --http=0.0.0.0:80 --wsgi-file=/app.py --callable=app
