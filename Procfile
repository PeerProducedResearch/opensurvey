release: python manage.py migrate
web: gunicorn open_survey.wsgi:application --log-file -
