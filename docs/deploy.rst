Deploy
========

This is where you describe how the project is deployed in production.

To setup a user and machine, these tutorials were used:
https://www.digitalocean.com/community/tutorials/initial-server-setup-with-ubuntu-16-04
https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-16-04
This includes the work to enable the firewall.


To setup haystack and solr:

::

    curl -LO https://archive.apache.org/dist/lucene/solr/x.Y.0/solr-X.Y.0.tgz
    mkdir solr
    tar -C solr -xf solr-X.Y.0.tgz --strip-components=1
    cd solr
    ./bin/solr start                                    # start solr
    ./bin/solr create -c tester -n basic_config         # create core named 'tester'
    ./manage.py build_solr_schema --configure-directory=<CoreConfigDif>
    ./manage.py rebuild_index
    ./bin/solr restart


The following env variables are required:

::

    DATABASE_URL
    DJANGO_SECRET_KEY
    DJANGO_ADMIN_URL
    DJANGO_ALLOWED_HOSTS
    REDIS_URL
    DJANGO_AWS_ACCESS_KEY_ID
    DJANGO_AWS_SECRET_ACCESS_KEY
    DJANGO_AWS_STORAGE_BUCKET_NAME
    DJANGO_SERVER_EMAIL
    EMAIL_FROM
    MAILGUN_API_KEY
    MAILGUN_DOMAIN

They are currently setup in a .env file in the project directory. In order to use this,
the setting ``DJANGO_READ_DOT_ENV_FILE`` needs to be set. This was accomplished by editing
the ``activate`` file of the virtualenv and adding the following code below the
``VIRTUAL_ENV`` variable.

::

    ...
    export VIRTUAL_ENV

    DJANGO_READ_DOT_ENV_FILE="True"
    export DJANGO_READ_DOT_ENV_FILE

    DJANGO_SETTINGS_MODULE="config.settings.production"
    export DJANGO_SETTINGS_MODULE
    ...


