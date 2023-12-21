# Useful commands

* Install project requirements:

~~~bash
pip install -r requirements.txt
~~~

* For the project creation it was used:

~~~bash
django-admin startproject core
~~~

* Create migrations:

~~~bash
python manage.py makemigrations
~~~

* Migrate changes (create tables in the specified database):

~~~bash
python manage.py migrate
~~~

* Create an app:

~~~bash
python manage.py startapp app_1
~~~

* Create superuser:

~~~bash
python manage.py createsuperuser
~~~

* Change password:

~~~bash
python manage.py changepassword <username>
~~~

* Run server in debug mode:

~~~bash
python manage.py runserver 
~~~

* Export db data to a json file:

~~~bash
python manage.py dumpdata > db.json
~~~

* Import db data from a json file:

~~~bash
python manage.py loaddata db.json
~~~

* Launch testing: (coverage included)

~~~bash
python manage.py test
~~~

* Generate html with coverage report:

~~~bash
coverage html
~~~

* Create static files (also used to upload static files to s3 bucket):

~~~bash
python manage.py collectstatic
~~~

* Upload default media files to s3 bucket:

~~~bash
python manage.py collectmedia
~~~

* Create static and media buckets:

~~~bash
python manage.py createbuckets
~~~

* Schedule users deletion task:

~~~bash
python manage.py schedule_users_delete
~~~

* Launch celery for development:

~~~bash
celery -A core worker -l INFO -P eventlet --scheduler django_celery_beat.schedulers:DatabaseScheduler
~~~

> ***redis*** must be launched too

* Generate locale messages files

~~~bash
django-admin makemessages --all --ignore=en
~~~

> Before executing it, a locale folder with all languages folders inside must be created

* Generate compiled messages

~~~bash
django-admin compilemessages --ignore=env
~~~

* Useful commands with docker compose
~~~bash
docker-compose run --entrypoint "sh" balhom-api-djangorest -c "python manage.py migrate"
docker-compose run --entrypoint "sh" balhom-api-djangorest -c "python manage.py createbuckets"
docker-compose run --entrypoint "sh" balhom-api-djangorest -c "python manage.py collectstatic --no-input"
docker-compose run --entrypoint "sh" balhom-api-djangorest -c "python manage.py collectmedia"
docker-compose run --entrypoint "sh" balhom-api-djangorest -c "python manage.py createsuperuser"
~~~
