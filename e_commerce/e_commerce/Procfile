web: gunicorn e_commerce.wsgi --log-file - 
#or works good with external database
web: python manage.py migrate && gunicorn e_commerce.wsgi