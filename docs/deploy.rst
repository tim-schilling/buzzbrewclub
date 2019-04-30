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
