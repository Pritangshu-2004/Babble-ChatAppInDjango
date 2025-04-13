web: gunicorn WebChat.wsgi --log-file - 
#or works good with external database
web: python manage.py migrate && gunicorn WebChat.wsgi