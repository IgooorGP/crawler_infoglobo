# starts gunicorn web server (more robust)
echo [LOG]: starting Gunicorn server...
echo [LOG]: listening on port 8000...

exec gunicorn crawler_app.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3
