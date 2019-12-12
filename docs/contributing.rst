Contributing
============

This section describes how to get running locally. You will
need Python v3.8 and PostgreSQL installed.

Create a .env file with the following content::

    DATABASE_URL=postgres://buzzbrewclub:buzzbrewclub@127.0.0.1:5432/buzzbrewclub

**DO NOT USE THESE VALUES ON A PRODUCTION SERVER**

Database
========
Create your database via::

    psql> CREATE DATABASE buzzbrewclub;
    psql> CREATE USER buzzbrewclub WITH ENCRYPTED PASSWORD 'buzzbrewclub';
    psql> GRANT ALL PRIVILEGES ON DATABASE buzzbrewclub TO buzzbrewclub;


Application
===========
* Create a virtual environment with ``virtualenv`` and activate it.
   * https://virtualenv.pypa.io/en/stable/
* Update your virtualenv's activate file (``<virtualenv>/bin/activate``)
  to enable reading from the .env file.

::

    ...
    export VIRTUAL_ENV

    DJANGO_READ_DOT_ENV_FILE="True"
    export DJANGO_READ_DOT_ENV_FILE
    ...

* Install dependencies::

    $ pip install -r requirements/local.txt

* Initialize the database::

    $ ./manage.py migrate

* Create a superuser account::

    $ ./manage.py createsuperuser

* Start your application::

    $ ./manage.py runserver

