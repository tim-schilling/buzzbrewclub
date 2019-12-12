Deploy
========

This is where you describe how the project is deployed in production.

To setup a user and machine, these tutorials were used:

* https://www.digitalocean.com/community/tutorials/initial-server-setup-with-ubuntu-16-04
* https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-16-04

This includes the work to enable the firewall.

Enable HTTPS with Let's Encrypt with the following tutorial:

* https://www.digitalocean.com/community/tutorials/how-to-secure-nginx-with-let-s-encrypt-on-ubuntu-16-04


To install Java:

::

    sudo apt-get install openjdk-8-jdk
    echo "JAVA_HOME=/usr/lib/jvm/java-XXX" | sudo tee -a /etc/environment


To setup haystack and solr:

::

    # Edit Solr config
    sudo nano /etc/default/solr.in.sh
    # Replace SOLR_JAVA_HOME with the JAVA_HOME variable from above.

    curl -LO https://archive.apache.org/dist/lucene/solr/6.6.6/solr-6.6.6.tgz
    mkdir solr
    tar -C solr -xf solr-6.6.6.tgz --strip-components=1
    sudo bash ./bin/install_solr_service.sh ../solr-6.6.6.tgz
    sudo systemctl enable solr solr.service                                  # start solr on startup
    sudo su - solr -c "/opt/solr/bin/solr create -c tester -n basic_config"  # create core named 'tester'
    ./manage.py build_solr_schema --configure-directory=<CoreConfigDif>
    ./manage.py rebuild_index
    sudo service solr restart


The following env variables are required:

::

    RECAPTCHA_PUBLIC_KEY
    RECAPTCHA_PRIVATE_KEY
    DATABASE_URL
    DJANGO_ADMIN_URL
    DJANGO_ALLOWED_HOSTS
    DJANGO_AWS_ACCESS_KEY_ID
    DJANGO_AWS_SECRET_ACCESS_KEY
    DJANGO_AWS_STORAGE_BUCKET_NAME
    DJANGO_SECRET_KEY
    DJANGO_SERVER_EMAIL
    EMAIL_FROM
    MAILGUN_API_KEY
    MAILGUN_DOMAIN
    REDIS_URL

They are currently setup in a .env file in the project directory. In order to use this,
the setting ``DJANGO_READ_DOT_ENV_FILE`` needs to be set. This was accomplished by editing
the ``activate`` file of the virtualenv and adding the following code below the
``VIRTUAL_ENV`` variable. This will support opening a shell or running commands.

::

    ...
    export VIRTUAL_ENV

    DJANGO_READ_DOT_ENV_FILE="True"
    export DJANGO_READ_DOT_ENV_FILE

    DJANGO_SETTINGS_MODULE="config.settings.production"
    export DJANGO_SETTINGS_MODULE
    ...

Create a .env.gunicorn file with the following settings to support the web application.


::

    DJANGO_READ_DOT_ENV_FILE="True"
    DJANGO_SETTINGS_MODULE="config.settings.production"

Email Settings
==============

All accounts are currently setup with the email schilling711+buzz@gmail.com

The email provider is MailGun and dmarc settings are configured at https://us.dmarcian.com

The domain buzzbrew.club is owned by Tim Schilling - schilling711+buzz@gmail.com.

Captcha Settings
================
These settings are currently configured by schillingt@better-simple.com
