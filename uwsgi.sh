uwsgi --http :6540 --wsgi-file app.wsgi --master --daemonize ./uwsgi_youtube.log --pidfile ./pid_5001.pid --workers 4 --threads 10
